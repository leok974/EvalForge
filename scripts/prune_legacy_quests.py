#!/usr/bin/env python3
"""
Identifies and optionally archives legacy quests that are not in the canonical questpack allowlist.

Usage:
    python scripts/prune_legacy_quests.py --dry-run  # Generate artifacts only
    python scripts/prune_legacy_quests.py --apply    # Archive legacy quests in DB
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add root to pythonpath
sys.path.append(os.getcwd())

from sqlalchemy import text
from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import QuestDefinition


def load_canonical_slugs():
    """Load slugs from canonical questpacks in allowlist."""
    allowlist_path = Path("configs/questpacks_active.json")
    
    if not allowlist_path.exists():
        print(f"❌ Allowlist not found: {allowlist_path}")
        return set()
    
    canonical_slugs = set()
    
    try:
        with open(allowlist_path, "r", encoding="utf-8") as f:
            allowlist_data = json.load(f)
        
        questpack_paths = allowlist_data.get("active_questpacks", [])
        
        for pack_path in questpack_paths:
            full_path = Path(pack_path)
            if not full_path.exists():
                print(f"⚠️  Questpack not found: {full_path}, skipping")
                continue
            
            with open(full_path, "r", encoding="utf-8") as f:
                pack_data = json.load(f)
            
            # Handle different questpack formats
            quests = []
            if isinstance(pack_data, list):
                quests = pack_data
            elif isinstance(pack_data, dict):
                if "quests" in pack_data:
                    quests = pack_data["quests"]
                elif "items" in pack_data:
                    quests = pack_data["items"]
                elif "quest_definitions" in pack_data:
                    quests = pack_data["quest_definitions"]
            
            for quest in quests:
                if isinstance(quest, dict):
                    slug = quest.get("slug") or quest.get("id") or quest.get("quest_path", "").split("/")[-1]
                    if slug:
                        canonical_slugs.add(slug)
                elif isinstance(quest, str):
                    canonical_slugs.add(quest)
        
        print(f"✅ Loaded {len(canonical_slugs)} canonical quest slugs from {len(questpack_paths)} questpacks")
        return canonical_slugs
    
    except Exception as e:
        print(f"❌ Failed to load canonical slugs: {e}")
        return set()


async def get_db_slugs():
    """Fetch all quest slugs from database."""
    async for session in get_session():
        result = await session.execute(select(QuestDefinition.slug))
        slugs = {row[0] for row in result.all()}
        print(f"✅ Found {len(slugs)} quests in database")
        return slugs


def generate_artifacts(legacy_slugs, canonical_slugs, db_slugs):
    """Generate JSON and Markdown artifacts listing legacy quests."""
    
    # JSON artifact
    json_data = {
        "timestamp": datetime.now().isoformat(),
        "canonical_count": len(canonical_slugs),
        "db_count": len(db_slugs),
        "legacy_count": len(legacy_slugs),
        "legacy_slugs": sorted(list(legacy_slugs)),
        "canonical_slugs": sorted(list(canonical_slugs))
    }
    
    json_path = Path("artifacts/legacy_quests_to_archive.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)
    
    print(f"📄 Generated JSON artifact: {json_path}")
    
    # Markdown artifact
    md_lines = [
        "# Legacy Quests to Archive",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Summary",
        "",
        f"- **Canonical quests**: {len(canonical_slugs)}",
        f"- **Database quests**: {len(db_slugs)}",
        f"- **Legacy quests** (to archive): {len(legacy_slugs)}",
        "",
        "## Legacy Quest Slugs",
        ""
    ]
    
    if legacy_slugs:
        for slug in sorted(legacy_slugs):
            md_lines.append(f"- `{slug}`")
    else:
        md_lines.append("*No legacy quests found*")
    
    md_lines.extend([
        "",
        "## Canonical Quest Slugs",
        ""
    ])
    
    for slug in sorted(canonical_slugs):
        md_lines.append(f"- `{slug}`")
    
    md_path = Path("artifacts/legacy_quests_to_archive.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    
    print(f"📄 Generated Markdown artifact: {md_path}")


async def archive_legacy_quests(legacy_slugs):
    """Archive legacy quests in database."""
    if not legacy_slugs:
        print("✅ No legacy quests to archive")
        return
    
    async for session in get_session():
        print(f"\n🗂️  Archiving {len(legacy_slugs)} legacy quests...")
        
        legacy_list = list(legacy_slugs)
        await session.execute(
            text("""
                UPDATE questdefinition
                SET is_archived = TRUE,
                    archived_at = NOW(),
                    archived_reason = 'legacy prune: not in active questpacks'
                WHERE slug = ANY(:slugs)
            """),
            {"slugs": legacy_list}
        )
        await session.commit()
        
        print(f"✅ Successfully archived {len(legacy_slugs)} legacy quests")
        print("\nArchived quests will no longer appear in:")
        print("  - Workshop quest list (default view)")
        print("  - QA dashboard (default view)")
        print("  - Coverage audits (unless --include-archived)")
        print("\nQuest history and attempt data preserved.")


async def main():
    import argparse
    parser = argparse.ArgumentParser(description='Identify and archive legacy quests not in canonical questpacks')
    parser.add_argument('--dry-run', action='store_true', help='Generate artifacts only, do not modify database')
    parser.add_argument('--apply', action='store_true', help='Archive legacy quests in database')
    args = parser.parse_args()
    
    if not args.dry_run and not args.apply:
        print("Please specify --dry-run or --apply")
        return
    
    print("🔍 Loading canonical quest slugs...")
    canonical_slugs = load_canonical_slugs()
    
    if not canonical_slugs:
        print("❌ No canonical slugs loaded, aborting")
        return
    
    print("\n🔍 Fetching database quest slugs...")
    db_slugs = await get_db_slugs()
    
    # Compute legacy slugs
    legacy_slugs = db_slugs - canonical_slugs
    
    print(f"\n📊 Analysis:")
    print(f"   Canonical: {len(canonical_slugs)}")
    print(f"   Database: {len(db_slugs)}")
    print(f"   Legacy (to archive): {len(legacy_slugs)}")
    
    # Generate artifacts
    print("\n📝 Generating artifacts...")
    generate_artifacts(legacy_slugs, canonical_slugs, db_slugs)
    
    if args.apply:
        print("\n🚨 Archiving legacy quests...")
        await archive_legacy_quests(legacy_slugs)
    else:
        print("\n✅ Dry-run complete. Use --apply to archive legacy quests in database.")


if __name__ == "__main__":
    asyncio.run(main())

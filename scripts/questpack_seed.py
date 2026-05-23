import asyncio
import json
import sys
import os
import glob
from pathlib import Path

# Add root to pythonpath
sys.path.append(os.getcwd())

from sqlalchemy import text
from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import QuestDefinition

def find_json_files(root_dir):
    """Recursively find all .json files in relevant directories."""
    patterns = [
        os.path.join(root_dir, "data", "questpacks", "**", "*.json"),
        os.path.join(root_dir, "seed", "**", "*.json"),
        os.path.join(root_dir, "docs", "quests", "**", "*.json"),
    ]
    files = []
    for p in patterns:
        files.extend(glob.glob(p, recursive=True))
    return sorted(list(set(files)))

async def seed_quest_pack(file_path, seeded_slugs=None):
    print(f"Seeding from {file_path}...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load JSON: {e}")
        return False

    # Normalize data to a list of quest objects
    quests = []
    
    # Context from Pack
    pack_world_id = None
    pack_track_id = None
    
    if isinstance(data, list):
        quests = data
    elif isinstance(data, dict):
        pack_world_id = data.get("world_id")
        pack_track_id = data.get("track_id")
        
        if "packs" in data:
            quests.extend(data["packs"])
        elif "quests" in data:
            quests.extend(data["quests"])
        elif "slug" in data or "id" in data: # Single quest object
            quests.append(data)
        else:
             # Might be a snapshot format with worlds/tracks, skip or handle?
             # For now, if it doesn't look like a quest list, we log and skip to avoid crashing
             print(f"  ⚠️ Unknown JSON structure in {file_path}, skipping.")
             return False

    if not quests:
        print(f"  ⚠️ No quests found in {file_path}.")
        return True

    async for session in get_session():
        # Ensure columns exist (Naive Migration)
        # Note: order_index and tier columns already exist in the model (default 0 / 1)
        try:
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS starter_code TEXT"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS objectives_json JSONB"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS tiered_hints_json JSONB"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS runtime_rules_json JSONB"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS language VARCHAR DEFAULT 'python'"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS workspace_json JSONB DEFAULT '{}'"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS grading_json JSONB DEFAULT '{}'"))
            
            # Phase 9.8 Parity
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS briefing_md TEXT"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS lore_md TEXT"))
            
            await session.commit()
        except Exception as e:
             await session.rollback()

        for position, quest_data in enumerate(quests):
            if not isinstance(quest_data, dict):
                continue
                
            slug = quest_data.get("slug")
            if not slug:
                # Try id
                slug = quest_data.get("id")
                
            if not slug:
                 continue

            print(f"  Upserting {slug}...")
            if seeded_slugs is not None:
                seeded_slugs.add(slug)
            
            # Check existing
            stmt = select(QuestDefinition).where(QuestDefinition.slug == slug)
            existing = (await session.exec(stmt)).first()
            
            # Defaults
            world_id = quest_data.get("world_id") or quest_data.get("world_slug") or pack_world_id
            track_id = quest_data.get("track_id") or quest_data.get("track_slug") or pack_track_id
            
            # If we are upserting and have existing, don't overwrite with None/Defaults if existing is valid
            if existing:
                world_id = world_id or existing.world_id
                track_id = track_id or existing.track_id
            
            # Final fallback
            world_id = world_id or "unknown"
            track_id = track_id or "misc"
            title = quest_data.get("title") or slug
            
            # Phase Q Fix: Secure workspace hydration from data/quests/<slug>/workspace
            def hydrate_workspace(q_slug):
                ws = {"files": []}
                root_d = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                w_dir = os.path.join(root_d, "data", "quests", q_slug, "workspace")
                if os.path.exists(w_dir):
                    for root, _, files in os.walk(w_dir):
                        for fname in files:
                            full_path = os.path.join(root, fname)
                            inner_path = os.path.relpath(full_path, w_dir)
                            try:
                                with open(full_path, "r", encoding="utf-8") as f:
                                    ws["files"].append({
                                        "path": inner_path.replace("\\", "/"),
                                        "content": f.read(),
                                        "editable": True
                                    })
                            except Exception as e:
                                print(f"    ⚠️ Failed to read {full_path}: {e}")
                return ws

            # order_index: prefer explicit value in JSON, fall back to list position
            # Gap #2 fix: ensures quests sort correctly within a track
            order_index = quest_data.get("order_index") or quest_data.get("order") or position

            # tier: visual difficulty grouping (1=foundry, 2=advanced, 3=expert, 4=mastery)
            tier = int(quest_data.get("tier") or 1)

            if not existing:
                existing = QuestDefinition(
                    slug=slug,
                    world_id=world_id,
                    track_id=track_id,
                    title=title,
                    short_description=quest_data.get("short_description", ""),
                    language=quest_data.get("language", "python"),
                    order_index=order_index,
                    tier=tier,
                )
                session.add(existing)
            else:
                 existing.world_id = world_id
                 existing.track_id = track_id
                 existing.title = title
                 existing.order_index = order_index
                 existing.tier = tier
                 if "language" in quest_data:
                     existing.language = quest_data["language"]
                 if "key_terms" in quest_data:
                     existing.key_terms = quest_data["key_terms"]
                 if "concept_tags" in quest_data:
                     existing.concept_tags = quest_data["concept_tags"]
            
            # Context for relative paths
            json_dir = os.path.dirname(os.path.abspath(file_path))

            # Helper to hydrate tutorial content
            # Strategy: 
            # 1. Check docs/quests/{slug}/ FIRST (authoring overlay)
            # 2. Then check files_from dir
            # 3. Then json_dir
            def hydrate_tutorial(q_obj, base_dir, q_data):
                slug = q_data.get("slug") or q_data.get("id")
                
                # Build search directories in priority order
                search_dirs = []
                
                # 1. Priority: docs/quests/{slug}/ overlay (authoring source of truth)
                root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                overlay_dir = os.path.join(root_dir, "docs", "quests", slug)
                if os.path.exists(overlay_dir):
                    search_dirs.append(overlay_dir)
                    print(f"    Checking overlay directory: {overlay_dir}")
                
                # 2. files_from directory (if specified)
                ws = q_data.get("workspace") or {}
                if "files_from" in ws:
                    files_from_dir = os.path.join(base_dir, ws["files_from"])
                    if os.path.exists(files_from_dir):
                        search_dirs.append(files_from_dir)
                
                # 3. Data Quests Directory (modern source)
                data_q_dir = os.path.join(root_dir, "data", "quests", slug)
                if os.path.exists(data_q_dir):
                    search_dirs.append(data_q_dir)
                    print(f"    Checking data directory: {data_q_dir}")

                # 4. JSON directory (fallback)
                search_dirs.append(base_dir)
                
                # Look for tutorial.md
                found_tutorial = False
                for d in search_dirs:
                    if found_tutorial: break
                    # Priority A: Check for tutorial.md in a 'docs' subfolder
                    docs_sub = os.path.join(d, "docs")
                    tut_paths = [
                        os.path.join(docs_sub, "tutorial.md"),
                        os.path.join(d, "tutorial.md")
                    ]
                    
                    for tut_path in tut_paths:
                        if os.path.exists(tut_path):
                            print(f"    ✅ Found tutorial.md in {os.path.dirname(tut_path)}")
                            try:
                                with open(tut_path, "r", encoding="utf-8") as f:
                                    q_obj.tutorial_md = f.read()
                                found_tutorial = True
                                break # Found it
                            except Exception as e:
                                print(f"    ⚠️ Failed to read tutorial {tut_path}: {e}")

                # Look for terms.json
                for d in search_dirs:
                    docs_sub = os.path.join(d, "docs")
                    terms_paths = [
                        os.path.join(docs_sub, "terms.json"),
                        os.path.join(d, "terms.json")
                    ]
                    for terms_path in terms_paths:
                        if os.path.exists(terms_path):
                            print(f"    ✅ Found terms.json in {os.path.dirname(terms_path)}")
                            try:
                                with open(terms_path, "r", encoding="utf-8") as f:
                                    terms_data = json.load(f)
                                    
                                    # Auto-derive refs (Handle List vs Dict)
                                    derived = []
                                    if isinstance(terms_data, list):
                                        for t in terms_data:
                                            if isinstance(t, dict) and t.get("codex_ref"):
                                                ref = t["codex_ref"]
                                                # Smart Prefixing logic
                                                if not ref.startswith("codex:"):
                                                    # If it looks like a glossary term and no path, try to guess
                                                    if "/" not in ref:
                                                        if q_obj.world_id == "world-sql":
                                                            ref = f"glossary/sql/{ref}"
                                                        else:
                                                            ref = f"concepts/{ref}"
                                                    ref = f"codex:{ref}"
                                                t["codex_ref"] = ref # Update in-place
                                                derived.append(ref)
                                    elif isinstance(terms_data, dict):
                                        if "codex_references" in terms_data:
                                            for i, ref in enumerate(terms_data["codex_references"]):
                                                if not ref.startswith("codex:"):
                                                    if "/" not in ref:
                                                        if q_obj.world_id == "world-sql":
                                                            ref = f"glossary/sql/{ref}"
                                                        else:
                                                            ref = f"concepts/{ref}"
                                                    terms_data["codex_references"][i] = f"codex:{ref}"
                                            derived = terms_data["codex_references"]
                                    
                                    q_obj.key_terms = terms_data # Re-assign updated
                                    q_obj.codex_references = list(set(derived))  # Unique
                                break  # Stop after first match
                            except Exception as e:
                                print(f"    ⚠️ Failed to read terms {terms_path}: {e}")

            # Hydrate Tutorial (Standard Logic)
            # Prefer inline content from JSON; fall back to disk file.
            # Use truthiness check (not key-presence) so "tutorial_md": null still triggers hydration.
            inline_md = quest_data.get("tutorial_md")
            if inline_md:
                existing.tutorial_md = inline_md
            else:
                hydrate_tutorial(existing, json_dir, quest_data)

            # Hydrate Briefing & Lore (Prefer Disk Overlay)
            # We use the same search logic as hydrate_tutorial but for other files
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            overlay_dir = os.path.join(root_dir, "docs", "quests", slug)

            # Briefing
            briefing_paths = [
                os.path.join(overlay_dir, "docs", "briefing.md"),
                os.path.join(overlay_dir, "briefing.md"),
                os.path.join(root_dir, "data", "quests", slug, "docs", "briefing.md"),
                os.path.join(root_dir, "data", "quests", slug, "briefing.md")
            ]
            for bp in briefing_paths:
                if os.path.exists(bp):
                    print(f"    ✅ Found briefing.md in {os.path.dirname(bp)}")
                    with open(bp, "r", encoding="utf-8") as f:
                        existing.briefing_md = f.read()
                    break
            else:
                 if "briefing_md" in quest_data:
                    existing.briefing_md = quest_data["briefing_md"]

            # Lore
            lore_paths = [
                os.path.join(overlay_dir, "docs", "lore.md"),
                os.path.join(overlay_dir, "lore.md"),
                os.path.join(root_dir, "data", "quests", slug, "docs", "lore.md"),
                os.path.join(root_dir, "data", "quests", slug, "lore.md")
            ]
            for lp in lore_paths:
                if os.path.exists(lp):
                    print(f"    ✅ Found lore.md in {os.path.dirname(lp)}")
                    with open(lp, "r", encoding="utf-8") as f:
                        existing.lore_md = f.read()
                    break
            else:
                if "lore_md" in quest_data:
                    existing.lore_md = quest_data["lore_md"]
            
            # Hints (Parse markdown to JSON)
            hints_paths = [
                os.path.join(overlay_dir, "docs", "hints.md"),
                os.path.join(overlay_dir, "hints.md"),
                os.path.join(root_dir, "data", "quests", slug, "docs", "hints.md"),
                os.path.join(root_dir, "data", "quests", slug, "hints.md")
            ]
            for hp in hints_paths:
                if os.path.exists(hp):
                     print(f"    ✅ Found hints.md in {os.path.dirname(hp)}")
                     with open(hp, "r", encoding="utf-8") as f:
                         raw_hints = f.read()
                         existing.tiered_hints_json = {"markdown_source": raw_hints}
                     break
            
            # Featured Tables & DB explorer fields
            if "featured_tables" in quest_data:
                existing.featured_tables = quest_data["featured_tables"]
            if "db_engine" in quest_data:
                existing.db_engine = quest_data["db_engine"]
            
            # Engine Safety: Quests starting with 'postgres-' MUST use postgres engine
            if slug.startswith("postgres-"):
                existing.db_engine = "postgres"

            if "db_explorer_enabled" in quest_data:
                existing.db_explorer_enabled = quest_data["db_explorer_enabled"]
            if "db_explorer_mode" in quest_data:
                existing.db_explorer_mode = quest_data["db_explorer_mode"]
            if "objectives" in quest_data:
                existing.objectives_json = quest_data["objectives"]
            
            # Ensure key_terms from quest_data are synced if present (explicit override)
            if "key_terms" in quest_data:
                existing.key_terms = quest_data["key_terms"]
            if "concept_tags" in quest_data:
                existing.concept_tags = quest_data["concept_tags"]
            if "codex_references" in quest_data:
                existing.codex_references = quest_data["codex_references"]

            existing.workspace_json = hydrate_workspace(slug)
            
            session.add(existing)
        
        await session.commit()
        return True


def _require_purge_confirmation(args) -> None:
    if not args.purge:
        return
    if args.i_understand_this_deletes_data:
        return
    if os.getenv("EF_PURGE_CONFIRM") == "1":
        return
    raise SystemExit(
        "EF_PURGE_CONFIRM_REQUIRED: Refusing to run --purge without explicit confirmation.\n"
        "Use --i-understand-this-deletes-data OR set EF_PURGE_CONFIRM=1."
    )

def write_purge_artifacts(deleted_slugs: list[str], active_questpacks: list[str]) -> None:
    from datetime import datetime, timezone
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "deleted_count": len(deleted_slugs),
        "deleted_slugs": sorted(deleted_slugs),
        "active_questpacks": active_questpacks,
        "note": "Generated by scripts/questpack_seed.py --purge",
    }

    (artifacts_dir / "purge_deleted_quests.json").write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )

    md_lines = [
        "# Purge deleted quests",
        "",
        f"- Generated at (UTC): `{payload['generated_at']}`",
        f"- Deleted count: **{payload['deleted_count']}**",
        "",
        "## Active questpacks",
        *[f"- `{p}`" for p in active_questpacks],
        "",
        "## Deleted slugs",
    ]
    if deleted_slugs:
        md_lines.extend([f"- `{s}`" for s in sorted(deleted_slugs)])
    else:
        md_lines.append("_None_")

    (artifacts_dir / "purge_deleted_quests.md").write_text(
        "\n".join(md_lines) + "\n",
        encoding="utf-8",
    )

async def purge_legacy_quests(active_slugs, active_questpack_paths: list[str] | None = None):
    """Delete quests from DB that are not in the active set."""
    print("🧹 Purging legacy quests...")
    deleted_slugs = []
    
    async for session in get_session():
        stmt = select(QuestDefinition.slug)
        results = await session.exec(stmt)
        db_slugs = {row for row in results}
        
        legacy = db_slugs - active_slugs
        if not legacy:
            print("  ✨ DB is clean (no legacy quests found).")
            # Write empty artifact for consistency
            write_purge_artifacts([], active_questpack_paths or [])
            return 0

        print(f"  Found {len(legacy)} legacy quests to purge.")
        try:
            # Using text for bulk delete
            list_str = ", ".join([f"'{s}'" for s in legacy])
            await session.exec(text(f"DELETE FROM questdefinition WHERE slug IN ({list_str})"))
            await session.commit()
            
            deleted_slugs = list(legacy)
            print(f"  🗑️  Purged {len(deleted_slugs)} quests: {', '.join(sorted(deleted_slugs)[:5])}...")
        except Exception as e:
            print(f"  ❌ Purge failed: {e}")
            await session.rollback()
    
    write_purge_artifacts(deleted_slugs, active_questpack_paths or [])
    return len(deleted_slugs)


async def seed_all(root_dir):
    files = find_json_files(root_dir)
    print(f"Found {len(files)} JSON files to inspect.")
    seeded_slugs = set()
    for f in files:
        await seed_quest_pack(f, seeded_slugs=seeded_slugs)
    return seeded_slugs

async def seed_canonical(allowlist_path, include_legacy=False, purge=False):
    print(f"Loading canonical questpacks from {allowlist_path}...")
    try:
        with open(allowlist_path, "r", encoding="utf-8") as f:
            allowlist_data = json.load(f)
        canonical_packs = allowlist_data.get("active_questpacks", [])
        
        seeded_slugs = set()
        
        if canonical_packs:
            print(f"Found {len(canonical_packs)} canonical questpacks")
            success_count = 0
            for pack_path in canonical_packs:
                full_path = os.path.join(os.getcwd(), pack_path)
                if os.path.exists(full_path):
                    if await seed_quest_pack(full_path, seeded_slugs=seeded_slugs):
                        success_count += 1
                else:
                    print(f"⚠️  Questpack not found: {full_path}")
            
            print(f"\n✅ Seeded {success_count}/{len(canonical_packs)} canonical questpacks")
            
            if purge:
                await purge_legacy_quests(seeded_slugs, active_questpack_paths=canonical_packs)
                
            return
        else:
            print("⚠️  No canonical questpacks defined in allowlist, falling back to all questpacks")
    except Exception as e:
        print(f"⚠️  Failed to load allowlist: {e}, falling back to all questpacks") 


async def main():
    import argparse
    parser = argparse.ArgumentParser(description='Seed quest definitions into database')
    parser.add_argument('path', nargs='?', help='Path to a questpack JSON file or quest directory')
    parser.add_argument('--all', action='store_true', help='Seed all active questpacks from allowlist')
    parser.add_argument('--include-legacy', action='store_true', help='Include legacy questpacks when using --all')
    parser.add_argument('--purge', action='store_true', help='Purge quests from DB that are NOT in the active set (requires --all)')
    parser.add_argument('--i-understand-this-deletes-data', action='store_true', help='Required to run --purge unless EF_PURGE_CONFIRM=1 is set.')
    args = parser.parse_args()

    # Safety Check
    _require_purge_confirmation(args)

    if args.purge and not args.all:
        print("⚠️  --purge requires --all to be safe.")
        sys.exit(1)


    if args.all:
        # Load canonical questpacks from allowlist
        allowlist_path = os.path.join(os.getcwd(), "configs", "questpacks_active.json")
        
        if os.path.exists(allowlist_path) and not args.include_legacy:
            await seed_canonical(allowlist_path, purge=args.purge)
        elif args.include_legacy:
            print("🔓 Including legacy questpacks (--include-legacy flag set)")
            # Fallback or legacy mode: seed all discovered questpacks
            await seed_all(os.getcwd())

    elif args.path:
        await seed_quest_pack(args.path)
    else:
        print("Usage: python questpack_seed.py <path> OR python questpack_seed.py --all")
        print("  --all                Seed all active questpacks from allowlist")
        print("  --include-legacy     Include legacy questpacks when using --all")

if __name__ == "__main__":
    asyncio.run(main())

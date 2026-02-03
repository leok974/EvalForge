
import asyncio
import json
import sys
import os

# Add root to pythonpath
sys.path.append(os.getcwd())

from sqlalchemy import text
from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import QuestDefinition

async def get_active_slugs():
    """Load all slugs from active questpacks defined in config."""
    config_path = os.path.join("configs", "questpacks_active.json")
    if not os.path.exists(config_path):
        print(f"❌ Config not found: {config_path}")
        return set()

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    active_packs = config.get("active_questpacks", [])
    slugs = set()

    for pack_path in active_packs:
        if not os.path.exists(pack_path):
            print(f"⚠️  Active pack not found: {pack_path}")
            continue
            
        try:
            with open(pack_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            quests = []
            if isinstance(data, list):
                quests = data
            elif isinstance(data, dict):
                if "packs" in data:
                    quests = data["packs"]
                elif "quests" in data:
                    quests = data["quests"]
                elif "slug" in data:
                    quests = [data]
            
            for q in quests:
                if isinstance(q, dict):
                    slug = q.get("slug") or q.get("id")
                    if slug:
                        slugs.add(slug)
        except Exception as e:
            print(f"❌ Failed to parse {pack_path}: {e}")

    return slugs

async def get_db_slugs():
    """Fetch all quest slugs from the database."""
    slugs = set()
    async for session in get_session():
        stmt = select(QuestDefinition.slug)
        results = await session.exec(stmt)
        for row in results:
            slugs.add(row)
    return slugs

async def main():
    print("🔍 Audit: Legacy Quest Detection")
    print("================================")
    
    print("Loading active questpacks...")
    active_slugs = await get_active_slugs()
    print(f"✅ Found {len(active_slugs)} active quests defined in questpacks.")

    print("Fetching DB quests...")
    try:
        db_slugs = await get_db_slugs()
        print(f"✅ Found {len(db_slugs)} quests in database.")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return

    legacy_slugs = db_slugs - active_slugs
    
    print("\n📊 Results")
    print(f"  Active: {len(active_slugs)}")
    print(f"  In DB:  {len(db_slugs)}")
    
    if legacy_slugs:
        print(f"\n⚠️  Found {len(legacy_slugs)} LEGACY quests (in DB but not active):")
        for s in sorted(legacy_slugs):
            print(f"   - {s}")
        print(f"\n💡 To purge these, run: python scripts/questpack_seed.py --all --purge")
        sys.exit(1) # Non-zero exit code to signal "drift detected" in CI
    else:
        print("\n✅ DB is clean! (All DB quests are active)")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())

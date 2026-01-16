
import asyncio
import json
import sys
import os
from sqlalchemy import text
from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import QuestDefinition

# Add root to pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

async def seed_quest_pack(file_path):
    print(f"Seeding from {file_path}...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load JSON: {e}")
        return False

    async for session in get_session():
        # Ensure columns exist (Naive Migration)
        # This prevents crash if models.py is updated but DB isn't
        try:
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS starter_code TEXT"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS objectives_json JSONB"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS tiered_hints_json JSONB"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS runtime_rules_json JSONB"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS language VARCHAR DEFAULT 'python'"))
            # Phase 6: Multi-File
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS workspace_json JSONB DEFAULT '{}'"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS grading_json JSONB DEFAULT '{}'"))
            await session.commit()
            print("  ✅ Schema columns verified/added.")
        except Exception as e:
             print(f"  ⚠️ Schema check failed (might be fine): {e}")
             await session.rollback()

        for quest_data in data:
            slug = quest_data["slug"]
            print(f"  Upserting {slug}...")
            
            # Check existing
            stmt = select(QuestDefinition).where(QuestDefinition.slug == slug)
            existing = (await session.exec(stmt)).first()
            
            if not existing:
                existing = QuestDefinition(
                    slug=slug,
                    world_id=quest_data["world_id"],
                    track_id=quest_data["track_id"],
                    title=quest_data["title"],
                    short_description=quest_data.get("short_description", "")
                )
                session.add(existing)
            else:
                 # Update core fields if needed
                 existing.world_id = quest_data["world_id"]
                 existing.track_id = quest_data["track_id"]
                 existing.title = quest_data["title"]
            
            # Update Config Fields
            existing.starter_code = quest_data.get("starter_code")
            # JSON pack uses "objectives_json" to match DB model, or "objectives" as alias
            existing.objectives_json = quest_data.get("objectives_json") or quest_data.get("objectives") or []
            existing.tiered_hints_json = quest_data.get("tiered_hints_json") or quest_data.get("tiered_hints") or {}
            existing.runtime_rules_json = quest_data.get("runtime_rules_json") or quest_data.get("runtime") or {}
            existing.base_xp_reward = quest_data.get("base_xp_reward") or quest_data.get("xp_base") or 50
            existing.language = quest_data.get("language", "python")
            
            # Phase 6
            existing.workspace_json = quest_data.get("workspace") or {}
            existing.grading_json = quest_data.get("grading") or {}

            if "detailed_description" in quest_data:
                existing.detailed_description = quest_data["detailed_description"]
            elif "description" in quest_data:
                existing.detailed_description = quest_data["description"]
            
            session.add(existing)
        
        await session.commit()
        print("✅ Seeding complete!")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python questpack_seed.py <path_to_json>")
        sys.exit(1)
        
    path = sys.argv[1]
    asyncio.run(seed_quest_pack(path))

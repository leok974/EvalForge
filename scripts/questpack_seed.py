import asyncio
import json
import sys
import os
import glob
from pathlib import Path
from sqlalchemy import text
from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import QuestDefinition

# Add root to pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
    if isinstance(data, list):
        quests = data
    elif isinstance(data, dict):
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
        try:
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS starter_code TEXT"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS objectives_json JSONB"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS tiered_hints_json JSONB"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS runtime_rules_json JSONB"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS language VARCHAR DEFAULT 'python'"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS workspace_json JSONB DEFAULT '{}'"))
            await session.exec(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS grading_json JSONB DEFAULT '{}'"))
            await session.commit()
        except Exception as e:
             await session.rollback()

        for quest_data in quests:
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
            world_id = quest_data.get("world_id") or "unknown"
            track_id = quest_data.get("track_id") or "misc"
            title = quest_data.get("title") or slug
            
            # Helper to hydrate files from disk if "files_from" is set
            def hydrate_workspace(ws, base_dir):
                if not ws or "files_from" not in ws:
                    return ws
                
                # Check for files_from
                rel_path = ws["files_from"]
                target_dir = os.path.normpath(os.path.join(base_dir, rel_path))
                
                if not os.path.exists(target_dir):
                    print(f"    ⚠️ Warning: files_from path '{target_dir}' does not exist. Skipping hydration.")
                    return ws
                    
                if "files" not in ws:
                    ws["files"] = []
                    
                for root, _, files in os.walk(target_dir):
                    for fname in files:
                        full_path = os.path.join(root, fname)
                        # Relative to target_dir to keep structure inside workspace
                        inner_path = os.path.relpath(full_path, target_dir)
                        # Read content
                        try:
                            with open(full_path, "r", encoding="utf-8") as f:
                                content = f.read()
                                
                            # Avoid duplicates
                            if not any(f["path"] == inner_path for f in ws["files"]):
                                ws["files"].append({
                                    "path": inner_path,
                                    "content": content,
                                    "editable": True # Default to true for hydrated files
                                })
                        except Exception as e:
                            print(f"    ⚠️ Failed to read {full_path}: {e}")
                
                return ws

            if not existing:
                existing = QuestDefinition(
                    slug=slug,
                    world_id=world_id,
                    track_id=track_id,
                    title=title,
                    short_description=quest_data.get("short_description", "")
                )
                session.add(existing)
            else:
                 existing.world_id = world_id
                 existing.track_id = track_id
                 existing.title = title
            
            # Context for relative paths
            json_dir = os.path.dirname(os.path.abspath(file_path))

            # Update Config Fields
            existing.starter_code = quest_data.get("starter_code")
            existing.objectives_json = quest_data.get("objectives_json") or quest_data.get("objectives") or []
            existing.tiered_hints_json = quest_data.get("tiered_hints_json") or quest_data.get("tiered_hints") or {}
            existing.runtime_rules_json = quest_data.get("runtime_rules_json") or quest_data.get("runtime") or {}
            existing.base_xp_reward = quest_data.get("base_xp_reward") or quest_data.get("xp_base") or 50
            existing.language = quest_data.get("language", "python")
            
            raw_ws = quest_data.get("workspace") or {}
            existing.workspace_json = hydrate_workspace(raw_ws, json_dir)
            
            existing.grading_json = quest_data.get("grading") or {}

            if "detailed_description" in quest_data:
                existing.detailed_description = quest_data["detailed_description"]
            elif "description" in quest_data:
                existing.detailed_description = quest_data["description"]
            
            session.add(existing)
        
        await session.commit()
        return True

async def seed_all(root_dir):
    files = find_json_files(root_dir)
    print(f"Found {len(files)} JSON files to inspect.")
    seeded_slugs = set()
    for f in files:
        await seed_quest_pack(f, seeded_slugs=seeded_slugs)
    return seeded_slugs

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", help="Specific file to seed")
    parser.add_argument("--all", action="store_true", help="Seed all found in known dirs")
    parser.add_argument("--root", default=os.getcwd(), help="Root directory to search from")
    
    args = parser.parse_args()
    
    if args.all:
        asyncio.run(seed_all(args.root))
    elif args.path:
        asyncio.run(seed_quest_pack(args.path))
    else:
        print("Usage: python questpack_seed.py <path> OR python questpack_seed.py --all")

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
                
                # 3. JSON directory (fallback)
                search_dirs.append(base_dir)
                
                # Look for tutorial.md
                for d in search_dirs:
                    tut_path = os.path.join(d, "tutorial.md")
                    if os.path.exists(tut_path):
                        print(f"    ✅ Found tutorial.md in {d}")
                        try:
                            with open(tut_path, "r", encoding="utf-8") as f:
                                q_obj.tutorial_md = f.read()
                            break  # Stop after first match
                        except Exception as e:
                            print(f"    ⚠️ Failed to read tutorial {tut_path}: {e}")

                # Look for terms.json
                for d in search_dirs:
                    terms_path = os.path.join(d, "terms.json")
                    if os.path.exists(terms_path):
                        print(f"    ✅ Found terms.json in {d}")
                        try:
                            with open(terms_path, "r", encoding="utf-8") as f:
                                terms_data = json.load(f)
                                q_obj.key_terms = terms_data
                                q_obj.key_terms = terms_data
                                # Auto-derive refs
                                derived = [t.get("codex_ref") for t in terms_data if t.get("codex_ref")]
                                q_obj.codex_references = list(set(derived))  # Unique
                            break  # Stop after first match
                        except Exception as e:
                            print(f"    ⚠️ Failed to read terms {terms_path}: {e}")

            # Hydrate files
            if "tutorial.md" not in quest_data: # Only hydrate if not in JSON
                 hydrate_tutorial(existing, json_dir, quest_data)

            # Update Config Fields (Partial Update Support)
            if "starter_code" in quest_data:
                existing.starter_code = quest_data["starter_code"]
            
            if "objectives_json" in quest_data:
                existing.objectives_json = quest_data["objectives_json"]
            elif "objectives" in quest_data:
                existing.objectives_json = quest_data["objectives"]
                
            if "tiered_hints_json" in quest_data:
                existing.tiered_hints_json = quest_data["tiered_hints_json"]
            elif "tiered_hints" in quest_data:
                existing.tiered_hints_json = quest_data["tiered_hints"]
                
            if "runtime_rules_json" in quest_data:
                existing.runtime_rules_json = quest_data["runtime_rules_json"]
            elif "runtime" in quest_data:
                existing.runtime_rules_json = quest_data["runtime"]
                
            if "base_xp_reward" in quest_data:
                existing.base_xp_reward = quest_data["base_xp_reward"]
            elif "xp_base" in quest_data:
                existing.base_xp_reward = quest_data["xp_base"]
                
            if "language" in quest_data:
                existing.language = quest_data["language"]
            
            if "workspace" in quest_data:
                raw_ws = quest_data["workspace"]
                existing.workspace_json = hydrate_workspace(raw_ws, json_dir)
            
            if "grading" in quest_data:
                existing.grading_json = quest_data["grading"]

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

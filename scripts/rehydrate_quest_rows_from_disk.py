import sys
import os
import json
import asyncio
import argparse
from pathlib import Path
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath('.'))
from arcade_app.database import engine
from arcade_app.models import QuestDefinition
from scripts.utils_questpacks import get_all_quest_slugs
from scripts.seed_evalforge_universe import build_quest_workspace

DOCS_DIR = Path("docs")
QUESTS_DIR = Path("data/quests")

async def rehydrate_from_disk():
    print("💧 Rehydrating Quest Rows from Disk...\n")
    
    # Load manifest
    active_slugs = set()
    manifest_path = Path("data/seed/active_curriculum.json")
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            active_slugs = set(data.get("active_slugs", []))
            
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    rehydrated_count = 0
    total_updates = 0
    
    async with async_session() as session:
        result = await session.execute(select(QuestDefinition))
        quests = result.scalars().all()
        
        for q in quests:
            if q.slug in active_slugs:
                continue
                
            disk_path = QUESTS_DIR / q.slug
            disk_path_old = DOCS_DIR / "quests" / q.slug
            
            target_dir = disk_path if disk_path.exists() else disk_path_old
            
            if not target_dir.exists():
                continue
                
            updates = []
            
            # 1. Briefing
            has_briefing = bool(q.briefing_md and q.briefing_md.strip()) or bool(q.detailed_description and q.detailed_description.strip())
            if not has_briefing:
                briefing_file = target_dir / "briefing.md"
                if not briefing_file.exists():
                    briefing_file = target_dir / "tutorial.md"
                if briefing_file.exists():
                    q.briefing_md = briefing_file.read_text(encoding="utf-8")
                    updates.append("briefing_md")
                    
            # 2. Starter / Workspace
            has_starter = bool(q.starter_code and q.starter_code.strip())
            has_workspace = False
            if q.workspace_json and "files" in q.workspace_json:
                files = q.workspace_json["files"]
                if any(f.get("content", "").strip() or f.get("path") for f in files):
                    has_workspace = True
                    
            if not has_starter and not has_workspace:
                # Use the built-in workspace builder from seed script
                workspace = build_quest_workspace(target_dir, {"workspace": q.workspace_json})
                if workspace and "files" in workspace and len(workspace["files"]) > 0:
                    q.workspace_json = workspace
                    updates.append("workspace_json")
                    
                    # Try to extract a simple starter_code for compatibility
                    for file in workspace["files"]:
                        if "starter" in file["path"].lower() or file["path"] == "main.py" or file["path"] == "index.html" or file["path"] == "index.js":
                            q.starter_code = file["content"]
                            updates.append("starter_code")
                            break
                            
            # 3. Objectives
            has_objectives = bool(q.objectives_json and len(q.objectives_json) > 0)
            if not has_objectives:
                obj_file = target_dir / "objectives.json"
                config_file = target_dir / "config.json"
                if obj_file.exists():
                    try:
                        q.objectives_json = json.loads(obj_file.read_text(encoding="utf-8"))
                        updates.append("objectives_json")
                    except: pass
                elif config_file.exists():
                    try:
                        cfg = json.loads(config_file.read_text(encoding="utf-8"))
                        if "objectives" in cfg:
                            q.objectives_json = cfg["objectives"]
                            updates.append("objectives_json from config")
                    except: pass
                    
            if updates:
                print(f"[{q.slug}] Updated: {', '.join(updates)}")
                rehydrated_count += 1
                total_updates += len(updates)
                
        if rehydrated_count > 0:
            print(f"\nCommitting changes for {rehydrated_count} quests...")
            await session.commit()
            print("✅ Rehydration complete.")
        else:
            print("No missing fields could be rehydrated from disk.")

if __name__ == "__main__":
    asyncio.run(rehydrate_from_disk())

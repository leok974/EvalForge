import sys
import os
import json
import asyncio
import argparse
from pathlib import Path
from sqlmodel import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath('.'))
from arcade_app.database import engine
from arcade_app.models import QuestDefinition, QuestProgress
from scripts.utils_questpacks import get_all_quest_slugs

DOCS_DIR = Path("docs")
QUESTS_DIR = Path("data/quests")

async def prune_zombies(apply: bool):
    print(f"🧹 Pruning Zombie Quests (Apply: {apply})...\n")
    
    # 1. Load active curriculum to ignore blocking quests
    active_slugs = set()
    manifest_path = Path("data/seed/active_curriculum.json")
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            active_slugs = set(data.get("active_slugs", []))
            
    # 2. Get all referenced slugs everywhere
    referenced_slugs = get_all_quest_slugs()
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    zombies_to_delete = []
    
    async with async_session() as session:
        result = await session.execute(select(QuestDefinition))
        quests = result.scalars().all()
        
        for q in quests:
            if q.slug in active_slugs:
                continue # Skip blocking
                
            disk_path = QUESTS_DIR / q.slug
            disk_path_old = DOCS_DIR / "quests" / q.slug
            has_folder = disk_path.exists() or disk_path_old.exists()
            is_referenced = q.slug in referenced_slugs
            
            is_zombie = not has_folder and not is_referenced
            
            if is_zombie:
                zombies_to_delete.append(q)
                
        print(f"Found {len(zombies_to_delete)} zombies.")
        
        if apply:
            for z in zombies_to_delete:
                print(f"  Deleting `{z.slug}`...")
                await session.execute(delete(QuestProgress).where(QuestProgress.quest_id == z.id))
                await session.delete(z)
            await session.commit()
            print("✅ Zombie quests deleted successfully.")
        else:
            for z in zombies_to_delete:
                print(f"  [DRY-RUN] Will delete `{z.slug}`")
            print("ℹ️ Run with --apply to actually delete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Actually delete the quests from the database")
    args = parser.parse_args()
    asyncio.run(prune_zombies(args.apply))

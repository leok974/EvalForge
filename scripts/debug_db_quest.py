
import asyncio
from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import QuestDefinition
import sys
import os

sys.path.append(os.getcwd())

async def debug_db():
    print("--- DEBUGGING DB QUEST ---")
    async for session in get_session():
        slug = "first-sparks"
        print(f"👉 Querying for '{slug}'...")
        stmt = select(QuestDefinition).where(QuestDefinition.slug == slug)
        res = await session.exec(stmt)
        quest = res.first()
        
        if quest:
            print(f"✅ FOUND in DB:")
            print(f"   Slug: {quest.slug}")
            print(f"   World: {quest.world_id}")
            print(f"   Track: {quest.track_id}")
            print(f"   Title: {quest.title}")
        else:
            print(f"❌ NOT FOUND in DB for slug '{slug}'")
            
        # Check count of all quests in world-python
        stmt_world = select(QuestDefinition).where(QuestDefinition.world_id == "world-python")
        res_world = await session.exec(stmt_world)
        world_quests = res_world.all()
        print(f"🌍 Quests in 'world-python': {len(world_quests)}")
        if len(world_quests) > 0:
            print(f"   Sample: {[q.slug for q in world_quests[:5]]}")
            
        break

if __name__ == "__main__":
    asyncio.run(debug_db())

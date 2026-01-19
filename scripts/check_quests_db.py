import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import QuestDefinition

async def check_quests_db():
    print("Checking quests contents...")
    async for session in get_session():
        result = await session.execute(select(QuestDefinition))
        quests = result.scalars().all()
        print(f"\nTotal quests in database: {len(quests)}")
        
        if quests:
            print("\nQuests:")
            for q in quests:
                print(f"ID: {q.id} | Slug: {q.slug} | Track: {q.track_id} | World: {q.world_id}")
        else:
            print("No quests found.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(check_quests_db())

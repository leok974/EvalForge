import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from arcade_app.services.quest_visibility import get_active_quest_config

active_slugs, slug_map = get_active_quest_config()
print(f"Total active slugs: {len(active_slugs)}")

docker_slugs = [s for s in active_slugs if 'docker' in s or 'compose' in s]
print(f"Docker related active slugs: {docker_slugs}")

from arcade_app.database import engine, get_session
import asyncio
from sqlmodel import select
from arcade_app.models import QuestDefinition

async def main():
    async for session in get_session():
        stmt = select(QuestDefinition).where(QuestDefinition.world_id == 'world-docker')
        res = await session.exec(stmt)
        quests = res.all()
        print(f"Docker quests in DB: {len(quests)}")
        for q in quests:
            print(f"- {q.slug} (active: {q.slug in active_slugs})")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

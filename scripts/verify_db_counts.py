
import sys
import os
# Ensure root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arcade_app.database import get_session
from arcade_app.models import QuestDefinition, BossDefinition, TrackDefinition
from sqlalchemy import text
from sqlmodel import select, func

import asyncio

async def count_db():
    async for session in get_session():
        # WorldDefinition might not exist if it's not a table yet?
        # User said: print('db_worlds', db.query(WorldDefinition).count())
        # I should check if WorldDefinition exists in models first, user script imported it.
        # But `scripts/seed_evalforge_universe.py` commented:
        # "# World definition is implicitly just strings in Track/Quest/Boss models currently,"
        # However, user's verification script explicitly imports WorldDefinition.
        # Let's try to import it, if fail, we assume 0 or handle it.
        
        # WorldDefinition not implemented yet
        worlds = "N/A"

        tracks = (await session.exec(select(func.count()).select_from(TrackDefinition))).one()
        bosses = (await session.exec(select(func.count()).select_from(BossDefinition))).one()
        quests = (await session.exec(select(func.count()).select_from(QuestDefinition))).one()
        
        print(f"db_worlds: {worlds}")
        print(f"db_tracks: {tracks}")
        print(f"db_bosses: {bosses}")
        print(f"db_quests: {quests}")
        break # One session is enough

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(count_db())

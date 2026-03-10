import asyncio
import os
import json
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

import sys
sys.path.insert(0, os.path.abspath('.'))

from arcade_app.database import engine
from arcade_app.models import QuestDefinition, Profile
from arcade_app.progress_models import QuestProgressV2
from arcade_app.services.quest_visibility import get_active_quest_config
from arcade_app.quest_helper import quest_to_dict

async def debug_api():
    os.environ["DATABASE_URL"] = "postgresql+asyncpg://evalforge:evalforge@localhost:5435/evalforge"
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Mock user data (admin/leo)
        user_id = "leo"
        
        # Get active config
        active_slugs, slug_to_pack = get_active_quest_config()
        print(f"Active slugs total: {len(active_slugs)}")
        print(f"sql-order-by in active: {'sql-order-by' in active_slugs}")
        
        # Exact logic from routes_quests.py
        world_id = "world-sql"
        query = select(QuestDefinition).where(QuestDefinition.world_id == world_id)
        query = query.where(QuestDefinition.slug.in_(active_slugs))
        query = query.order_by(
            QuestDefinition.world_id,
            QuestDefinition.track_id,
            QuestDefinition.order_index
        )
        
        result = await session.execute(query)
        quests = result.scalars().all()
        
        print(f"Quests returned for world-sql: {len(quests)}")
        for i, q in enumerate(quests):
            print(f"{i+1}. {q.slug} (track: {q.track_id}, order: {q.order_index})")

if __name__ == "__main__":
    asyncio.run(debug_api())

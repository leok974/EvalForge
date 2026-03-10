import asyncio
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from arcade_app.database import engine
from arcade_app.models import QuestDefinition
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

async def check():
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        # Find all quests with "MISSING" in short_description
        res = await session.execute(
            select(QuestDefinition).where(QuestDefinition.short_description == "MISSING")
        )
        rows = res.scalars().all()
        print(f"Total quests with 'MISSING' description: {len(rows)}")
        print("-" * 60)
        print(f"{'Slug':<40} | {'World':<10} | {'Track'}")
        print("-" * 60)
        for r in rows:
            print(f"{r.slug:<40} | {r.world_id:<10} | {r.track_id}")

if __name__ == "__main__":
    asyncio.run(check())

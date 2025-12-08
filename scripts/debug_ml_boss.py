import asyncio
import os
from sqlmodel import select
from arcade_app.database import engine
from arcade_app.models import BossDefinition
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

async def check():
    # engine is imported globally
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        stmt = select(BossDefinition).where(BossDefinition.id == "boss-synapse-mlops-sentinel")
        result = await session.execute(stmt)
        boss = result.scalar_one_or_none()
        
        if boss:
            print(f"Boss Found: {boss.id}")
            print(f"Rubric: '{boss.rubric}'") # Quotes to see if empty
            print(f"Name: {boss.name}")
        else:
            print("Boss NOT Found")

if __name__ == "__main__":
    asyncio.run(check())

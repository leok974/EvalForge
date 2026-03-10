import asyncio
import json
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from arcade_app.models import QuestDefinition
from arcade_app.config import DATABASE_URL

async def check():
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        q = (await session.execute(select(QuestDefinition).where(QuestDefinition.slug == "sql-limit"))).scalar_one_or_none()
        if q:
            print(f"Hints JSON: {json.dumps(q.tiered_hints_json, indent=2)}")
        else:
            print("Quest not found")

if __name__ == "__main__":
    asyncio.run(check())

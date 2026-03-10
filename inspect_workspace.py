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
        for slug in ["sql-order-by", "sql-limit"]:
            q = (await session.execute(select(QuestDefinition).where(QuestDefinition.slug == slug))).scalar_one_or_none()
            if q:
                print(f"Slug: {q.slug}")
                print(f"Workspace JSON: {json.dumps(q.workspace_json, indent=2)}")
                print("-" * 20)
            else:
                print(f"{slug} not found")

if __name__ == "__main__":
    asyncio.run(check())

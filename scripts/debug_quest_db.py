import asyncio
import os
import json
from sqlmodel import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import sys

# Import models from app
sys.path.append(os.getcwd())
from arcade_app.models import QuestDefinition

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/arcade")

async def main():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    slug = "hello-variable"
    
    async with async_session() as session:
        stmt = select(QuestDefinition).where(QuestDefinition.slug == slug)
        result = await session.execute(stmt)
        quest = result.scalar_one_or_none()
        
        output = {}
        if not quest:
            output["error"] = "Quest not found"
        else:
            output["slug"] = quest.slug
            output["key_terms"] = quest.key_terms
            output["tiered_hints"] = quest.tiered_hints_json
            output["codex_references"] = quest.codex_references
            print(f"DEBUG: Codex Refs = {quest.codex_references}")
        
        with open("quest_dump.json", "w") as f:
            json.dump(output, f, indent=2)
        print("Done writing to quest_dump.json")

if __name__ == "__main__":
    asyncio.run(main())

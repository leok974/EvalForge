import asyncio
from sqlalchemy import text
from arcade_app.database import get_session

async def inspect_db():
    print("🔍 Inspecting KnowledgeChunk constraints...")
    async for session in get_session():
        result = await session.execute(text(
            "SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint WHERE conrelid = 'knowledgechunk'::regclass;"
        ))
        for row in result:
            print(f"  - {row[0]}: {row[1]}")

if __name__ == "__main__":
    asyncio.run(inspect_db())

import asyncio
import os
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

# Load DB config
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://evalforge:evalforge@127.0.0.1:5435/evalforge")

async def migrate():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        print("Checking for 'quick_fixes_json' column in 'quest_attempts' table...")
        # Check if column exists
        result = await conn.execute(text(
            "SELECT column_name FROM information_schema.columns WHERE table_name='quest_attempts' AND column_name='quick_fixes_json'"
        ))
        if result.scalar():
            print("Column 'quick_fixes_json' already exists. Skipping.")
        else:
            print("Adding 'quick_fixes_json' column...")
            await conn.execute(text("ALTER TABLE quest_attempts ADD COLUMN quick_fixes_json JSONB DEFAULT '[]'"))
            print("Migration complete.")

if __name__ == "__main__":
    asyncio.run(migrate())

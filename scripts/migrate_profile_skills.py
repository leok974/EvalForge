import asyncio
from sqlalchemy import text
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arcade_app.database import engine

async def migrate():
    async with engine.begin() as conn:
        print("Migrating Profile table...")
        try:
            await conn.execute(text("ALTER TABLE profile ADD COLUMN skill_points INTEGER DEFAULT 3"))
            print("✅ Added skill_points column.")
        except Exception as e:
            print(f"⚠️  Column might already exist: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(migrate())

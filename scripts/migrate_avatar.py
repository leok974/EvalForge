import asyncio
import sys
import os
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arcade_app.database import engine

async def migrate():
    print("🔄 Migrating User table...")
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE \"user\" ADD COLUMN IF NOT EXISTS current_avatar_id VARCHAR DEFAULT 'default_user';"))
            print("✅ Column 'current_avatar_id' added (or already exists).")
        except Exception as e:
            print(f"⚠️ Migration warning (might be already done): {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(migrate())

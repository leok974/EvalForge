import asyncio
import os
import sys
from sqlalchemy import text
from arcade_app.database import get_session

# Add root to pythonpath
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def migrate():
    print("🚀 Migrating QuestProgress schema for Stuck Detector...")
    async for session in get_session():
        try:
            # Add columns
            await session.exec(text("ALTER TABLE quest_progress ADD COLUMN IF NOT EXISTS fail_streak_runs INTEGER DEFAULT 0"))
            await session.exec(text("ALTER TABLE quest_progress ADD COLUMN IF NOT EXISTS fail_streak_submits INTEGER DEFAULT 0"))
            await session.exec(text("ALTER TABLE quest_progress ADD COLUMN IF NOT EXISTS repeat_failure_count INTEGER DEFAULT 0"))
            await session.exec(text("ALTER TABLE quest_progress ADD COLUMN IF NOT EXISTS last_primary_failure VARCHAR"))
            await session.exec(text("ALTER TABLE quest_progress ADD COLUMN IF NOT EXISTS last_success_at TIMESTAMP WITHOUT TIME ZONE"))
            await session.exec(text("ALTER TABLE quest_progress ADD COLUMN IF NOT EXISTS stuck_level INTEGER DEFAULT 0"))
            
            await session.commit()
            print("✅ Schema updated successfully.")
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            await session.rollback()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(migrate())

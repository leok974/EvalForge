import asyncio
from sqlalchemy import text
from arcade_app.database import get_session

async def fix_schema():
    print("🔧 Checking DB Schema...")
    async for session in get_session():
        try:
            # Try to add the column. If it exists, it might fail or we can use IF NOT EXISTS if supported (Postgres 9.6+)
            # SQLModel/SQLAlchemy JSON type usually maps to JSON in Postgres.
            print("  - Attempting to add metadata_json column...")
            await session.execute(text("ALTER TABLE knowledgechunk ADD COLUMN IF NOT EXISTS metadata_json JSON DEFAULT '{}'::json;"))
            
            print("  - Attempting to drop incorrect unique constraint on source_id...")
            await session.execute(text("ALTER TABLE knowledgechunk DROP CONSTRAINT IF EXISTS knowledgechunk_source_id_key;"))
            
            await session.commit()
            print("  ✅ Schema fixed.")
        except Exception as e:
            print(f"  ❌ Error: {e}")
            # If transaction aborted, rollback
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(fix_schema())

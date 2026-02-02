import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Fix auth: Override DATABASE_URL with credentials from docker-compose.yml
os.environ["DATABASE_URL"] = "postgresql+asyncpg://evalforge:evalforge@127.0.0.1:5435/evalforge"

from sqlalchemy import text
from arcade_app.database import get_session

async def fix_quest_schema():
    print("🔧 Fixing QuestDefinition Schema...")
    async for session in get_session():
        try:
            # 1. tutorial_md
            print("  - Checking/Adding 'tutorial_md'...")
            await session.execute(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS tutorial_md TEXT;"))
            
            # 2. key_terms
            print("  - Checking/Adding 'key_terms'...")
            # Use JSONB if postgres, or JSON. standard SQLModel uses JSON but pg driver usually prefers JSONB for efficiency if we index it. 
            # safe bet is JSON.
            await session.execute(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS key_terms JSON DEFAULT '[]'::json;"))

            # 3. concept_tags
            print("  - Checking/Adding 'concept_tags'...")
            await session.execute(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS concept_tags JSON DEFAULT '[]'::json;"))

            # 4. codex_references
            print("  - Checking/Adding 'codex_references'...")
            await session.execute(text("ALTER TABLE questdefinition ADD COLUMN IF NOT EXISTS codex_references JSON DEFAULT '[]'::json;"))

            await session.commit()
            print("  ✅ Schema fixed. Columns added if they were missing.")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            await session.rollback()
        break

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(fix_quest_schema())

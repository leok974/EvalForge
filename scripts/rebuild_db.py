import asyncio
import os
import sys

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel
from arcade_app.database import engine, init_db
# Import models to ensure they are registered
from arcade_app import models 

async def rebuild():
    print("⚠️  DESTROYING DATABASE (SCHEMA RESET)...")
    async with engine.begin() as conn:
        from sqlalchemy import text
        await conn.execute(text("DROP SCHEMA public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))
        await conn.execute(text("GRANT ALL ON SCHEMA public TO evalforge"))
        await conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
        
        # Re-enable extensions
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        
        # Re-create tables
        await conn.run_sync(SQLModel.metadata.create_all)
        
    print("✅ Database Reset & Re-initialized.")

if __name__ == "__main__":
    asyncio.run(rebuild())

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
    print("⚠️  DESTROYING DATABASE...")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    print("✅ Database Destroyed.")
    
    print("🔄 Initializing Database...")
    await init_db()
    print("✅ Database Re-initialized.")

if __name__ == "__main__":
    asyncio.run(rebuild())

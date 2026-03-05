import asyncio, os, sys
sys.path.insert(0, os.path.abspath('.'))
from arcade_app.database import engine
from sqlalchemy import text

async def patch():
    async with engine.begin() as conn:
        await conn.execute(text("UPDATE quest_definitions SET language='sql' WHERE slug='sql-select'"))
        print("Patched sql-select language to 'sql'")

asyncio.run(patch())

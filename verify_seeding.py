import asyncio
import os

# Force SQLite for local verification
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_seeding.db"

from arcade_app.database import engine, init_db
from arcade_app.seed_quests_standard_worlds import seed_standard_world_quests
from sqlmodel import select
from arcade_app.models import QuestDefinition

async def verify_seeding():
    # Clean up previous test db
    if os.path.exists("test_seeding.db"):
        os.remove("test_seeding.db")

    await init_db()
    
    print("Running seeder...")
    async with engine.begin() as conn:
        def run_seeder(connection):
            from sqlmodel import Session
            session = Session(bind=connection)
            seed_standard_world_quests(session)
            
        await conn.run_sync(run_seeder)
        
    print("Verifying quests...")
    async with engine.connect() as conn:
        # Check for a few expected quests
        slugs = ["python-ignition", "js-refraction", "infra-service-link"]
        for slug in slugs:
            # We need to run the query in sync context
            def check_slug(sync_conn):
                from sqlalchemy import text
                result = sync_conn.execute(text(f"SELECT count(*) FROM questdefinition WHERE slug = '{slug}'"))
                return result.scalar()
            
            count = await conn.run_sync(check_slug)
            if count == 1:
                print(f"✅ Found quest: {slug}")
            else:
                print(f"❌ Missing quest: {slug}")

if __name__ == "__main__":
    asyncio.run(verify_seeding())

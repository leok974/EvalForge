
from arcade_app.database import get_session
from arcade_app.models import Profile
from sqlmodel import select
import asyncio
import os

# Mock env if needed, but docker exec should have it
# os.environ["DATABASE_URL"] = ... 

async def main():
    print("Checking database content...")
    try:
        async for session in get_session():
            result = await session.exec(select(Profile))
            profiles = result.all()
            print(f"Profiles found: {len(profiles)}")
            for p in profiles:
                print(f" - User: {p.user_id}, XP: {p.total_xp}")
            break
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

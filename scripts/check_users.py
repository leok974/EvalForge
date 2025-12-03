import asyncio
from arcade_app.database import get_session
from sqlmodel import select
from arcade_app.models import User

async def main():
    print("Checking users...")
    async for session in get_session():
        result = await session.execute(select(User))
        users = result.scalars().all()
        for u in users:
            print(f"User: {u.name}, ID: {u.id}")

if __name__ == "__main__":
    asyncio.run(main())

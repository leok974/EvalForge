import asyncio
from arcade_app.database import get_session
from sqlmodel import select
from arcade_app.models import Project

async def main():
    print("Checking projects in DB...")
    async for session in get_session():
        result = await session.execute(select(Project))
        projects = result.scalars().all()
        print(f"Found {len(projects)} projects:")
        for p in projects:
            print(f"- {p.name} (User: {p.owner_user_id}, Repo: {p.repo_url})")

if __name__ == "__main__":
    asyncio.run(main())

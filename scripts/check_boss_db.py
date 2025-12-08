import asyncio
from sqlmodel import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from arcade_app.database import engine
from arcade_app.models import BossDefinition

async def check_boss():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        stmt = select(BossDefinition)
        result = await session.execute(stmt)
        bosses = result.scalars().all()
        
        print(f"Total Bosses: {len(bosses)}")
        for b in bosses:
            print(f" - {b.id}: {b.name}")

if __name__ == "__main__":
    import sys
    sys.path.append("d:/EvalForge")
    asyncio.run(check_boss())

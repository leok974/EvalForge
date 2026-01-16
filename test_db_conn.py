import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

url = "postgresql+asyncpg://evalforge_app:evalforge_dev@127.0.0.1:5435/evalforge"
engine = create_async_engine(url, echo=False, future=True)

async def main():
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            row = result.scalar()
            print(f"✅ SQLAlchemy async result: {row}")
            print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())

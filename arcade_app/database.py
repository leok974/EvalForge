import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Default to localhost if running outside docker, else use docker service name
# Note: For local dev (outside docker), you might need to change 'db' to 'localhost' in the URL
# or map 127.0.0.1 to db in hosts file.
DB_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://evalforge:evalforge@localhost:5432/evalforge")

engine = create_async_engine(DB_URL, echo=True, future=True)

async def init_db():
    """
    Creates tables if they don't exist.
    """
    async with engine.begin() as conn:
        # 1. Enable pgvector extension
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        
        # 2. Create Tables (In production, use Alembic)
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    """
    Dependency for FastAPI routes.
    """
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

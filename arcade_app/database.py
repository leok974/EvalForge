import os
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Import all models to ensure they're registered in SQLModel.metadata
# This must happen before init_db() is called
from arcade_app.models import (
    User, Profile, Project, ProjectCodexDoc, KnowledgeChunk,
    BossDefinition, BossRun, BossProgress, QuestDefinition, QuestProgress,
    SkillNode, UserSkill, AvatarDefinition, ChatSession, TrackDefinition
)

# Default to localhost if running outside docker, else use docker service name
# Note: For local dev (outside docker), you might need to change 'db' to 'localhost' in the URL
# or map 127.0.0.1 to db in hosts file.
DB_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://evalforge:evalforge@localhost:5432/evalforge")

engine = create_async_engine(DB_URL, echo=True, future=True)

import logging

logger = logging.getLogger(__name__)

async def init_db():
    """
    Creates tables if they don't exist.
    
    Debuggable version with comprehensive logging.
    """
    logger.info("init_db: starting")
    
    # Import models so they register with metadata
    from arcade_app import models as _models  # noqa: F401
    
    logger.info(
        "init_db: metadata tables BEFORE create_all = %s",
        list(SQLModel.metadata.tables.keys())[:10]  # First 10 for brevity
    )
    logger.info("init_db: total tables in metadata = %d", len(SQLModel.metadata.tables))
    logger.info("init_db: 'bossdefinition' in metadata = %s", 'bossdefinition' in SQLModel.metadata.tables)
    
    async with engine.begin() as conn:
        # 1. Enable pgvector extension (Postgres only)
        if engine.dialect.name == "postgresql":
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        
        # 2. Create Tables - MUST use run_sync for AsyncEngine
        logger.info("init_db: calling metadata.create_all(...)")
        await conn.run_sync(SQLModel.metadata.create_all)
        
        # 3. DEBUG: Verify tables in DB after create_all
        result = await conn.execute(
            text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema='public' ORDER BY table_name"
            )
        )
        tables = [row[0] for row in result]
        logger.info("init_db: tables in DB AFTER create_all = %s", tables[:15])
        logger.info("init_db: total tables in DB = %d", len(tables))
        logger.info("init_db: 'bossdefinition' in DB = %s", 'bossdefinition' in tables)
    
    logger.info("init_db: finished create_all(engine=%r)", engine.url)

async def get_session() -> AsyncSession:
    """
    Dependency for FastAPI routes.
    """
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

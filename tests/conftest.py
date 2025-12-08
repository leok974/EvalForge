import pytest
import pytest_asyncio
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from arcade_app import database
# Ensure models are registered with SQLModel.metadata
from arcade_app import models

from sqlalchemy.pool import StaticPool

# 1. Use In-Memory SQLite for fast testing
# (CheckSameThread=False is needed for sqlite + async)
# TEST_DB_URL = "sqlite+aiosqlite:///:memory:"
TEST_DB_URL = "sqlite+aiosqlite:///./test.db"

@pytest_asyncio.fixture(name="test_engine", scope="function")
async def engine_fixture():
    engine = create_async_engine(
        TEST_DB_URL, 
        connect_args={"check_same_thread": False}, 
        echo=False
    )
    
    # Create Tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    yield engine
    
    # Teardown
    async with engine.begin() as conn:
        await conn.execute(text("PRAGMA foreign_keys = OFF"))
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.execute(text("PRAGMA foreign_keys = ON"))
    
    await engine.dispose()

@pytest_asyncio.fixture(name="db_session")
async def session_fixture(test_engine):
    """
    Creates a new session for a test and monkeypatches the global engine
    so the helpers use this Test DB instead of Postgres.
    """
    # PATCHING: Swap the production engine for the test engine
    original_engine = database.engine
    database.engine = test_engine
    
    async_session = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
        
    # RESTORE: Put the prod engine back
    database.engine = original_engine

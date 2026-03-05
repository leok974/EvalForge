import pytest
import pytest_asyncio
import asyncio
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from arcade_app.models import QuestDefinition, TrackDefinition
from scripts.seed_evalforge_universe import upsert_track, upsert_quest
import json

@pytest_asyncio.fixture
async def async_session():
    # Use in-memory SQLite for testing SQLModel
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    
    # Create tables
    async with engine.begin() as conn:
        from sqlmodel import SQLModel
        await conn.run_sync(SQLModel.metadata.create_all)
        
    async_session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session_maker() as session:
        yield session
        
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest.mark.asyncio
async def test_seed_content_mapping(async_session):
    world_slug = "world-sql"
    track_id = "core-sql"
    
    # 1. Setup minimal track so quest can link to it (if foreign keys are enforced, though sqlite memory might not care)
    # Actually, let's just create the track just in case.
    track_data = {
        "track_id": track_id,
        "title": "Core SQL",
        "summary": "Test Track"
    }
    await upsert_track(async_session, world_slug, track_data)
    
    # 2. Build minimal fake quest JSON with non-empty string content
    quest_data = {
        "slug": "test-quest-mapping",
        "title": "Mapping Test",
        "description": "A very detailed description.",
        "language": "sql",
        "starter_code": "-- SELECT * FROM test;\n",
        "briefing_md": "## Welcome to the test briefing",
        "tutorial_md": "## Here is a tutorial",
        "lore_md": "## Deep lore",
        "objectives": [
            {
                "id": "tests_pass",
                "title": "Query returns correct result",
                "kind": "tests_pass"
            }
        ],
        "key_terms": [
            "glossary/sql/select",
            "glossary/sql/from"
        ],
        "workspace": {
            "files": [
                {"path": "task.sql", "content": ""}
            ]
        }
    }
    
    # 3. Upsert Quest
    await upsert_quest(async_session, quest_data, world_slug, track_id, seeded_slugs=set())
    await async_session.commit()
    
    # 4. Fetch the quest back and assert fields
    stmt = select(QuestDefinition).where(QuestDefinition.slug == f"{track_id}-{quest_data['slug']}")
    result = await async_session.execute(stmt)
    quest = result.scalar_one_or_none()
    
    assert quest is not None, "Quest was not inserted into the database"
    
    # Ensure mapping didn't drop strings
    assert quest.starter_code == quest_data["starter_code"], "Starter code mapping failed"
    assert quest.briefing_md == quest_data["briefing_md"], "Briefing MD mapping failed"
    assert quest.tutorial_md == quest_data["tutorial_md"], "Tutorial MD mapping failed"
    assert quest.lore_md == quest_data["lore_md"], "Lore MD mapping failed"
    
    # Objectives and Key Terms
    assert quest.objectives_json == quest_data["objectives"], "Objectives mapping failed"
    assert len(quest.objectives_json) == 1, "Objectives list should have 1 item"
    
    assert quest.key_terms == quest_data["key_terms"], "Key terms mapping failed"
    assert len(quest.key_terms) == 2, "Key terms should have 2 items"

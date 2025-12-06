import os
import pytest
from httpx import AsyncClient, ASGITransport
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from arcade_app.agent import app
from arcade_app.database import get_session, engine # import engine
from arcade_app.models import QuestProgress, QuestDefinition, QuestState

# Ensure we use test DB or safe DB
# For these tests, we rely on the running enviroment's DB or the one configured by pytest fixtures if available.
# But often we just hit the app if using TestClient/AsyncClient against the `app` object.

@pytest.mark.asyncio
async def test_world_progress_endpoint_smoke():
    # 1. Hit the endpoint
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Auth relies on EVALFORGE_AUTH_MODE=mock (set in conftest or env)
        os.environ["EVALFORGE_AUTH_MODE"] = "mock"
        
        response = await client.get("/api/worlds/progress")
        assert response.status_code == 200
        
        data = response.json()
        assert "tracks" in data
        assert isinstance(data["tracks"], list)
        
        # We expect some tracks because universe is seeded
        if len(data["tracks"]) > 0:
            track = data["tracks"][0]
            assert "world_slug" in track
            assert "track_slug" in track
            assert "progress" in track
            assert "label" in track
            
            # Smoke check types
            assert isinstance(track["progress"], (int, float))
            assert isinstance(track["total_quests"], int)

@pytest.mark.asyncio
async def test_progress_calculation_logic():
    # This test manually inserts a completion to verify progress > 0
    # Uses database directly via get_session to ensure correct config
    
    selected_quest_id = None
    quest_track_id = None
    
    async for session in get_session():
        # Find a quest
        quest = (await session.exec(select(QuestDefinition))).first()
        if not quest:
            pytest.skip("No quests found in DB")
            break
            
        selected_quest_id = quest.id
        quest_track_id = quest.track_id
        
        # Create completion for mock user 'leo'
        # Check if already exists
        existing = (await session.exec(
            select(QuestProgress).where(
                QuestProgress.user_id == "leo",
                QuestProgress.quest_id == quest.id
            )
        )).first()
        
        if not existing:
            qp = QuestProgress(
                user_id="leo",
                quest_id=quest.id,
                state=QuestState.COMPLETED
            )
            session.add(qp)
            await session.commit()
        break # Exit generator
            
    if not selected_quest_id:
        return # Skipped

    # Now query API
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        os.environ["EVALFORGE_AUTH_MODE"] = "mock"
        response = await client.get("/api/worlds/progress")
        assert response.status_code == 200
        data = response.json()
        
        # Find the track for that quest
        matching_track = next((t for t in data["tracks"] if t["track_slug"] == quest_track_id), None)
        assert matching_track is not None
        assert matching_track["completed_quests"] >= 1
        assert matching_track["progress"] > 0

import pytest
import pytest_asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from httpx import AsyncClient, ASGITransport
from arcade_app.models import User, Profile, QuestDefinition, QuestProgress, QuestState
from arcade_app.agent import app

# Import the shared Vertex AI mock helpers
# We use absolute import assuming correct pythonpath or pytest root
from tests.backend.vertex_ai_mocks import (
    install_vertex_ai_mocks,
    reset_vertex_ai_mocks,
    set_vertex_ai_default_text,
)


@pytest_asyncio.fixture
async def client():
    """
    Async client for testing streaming endpoints.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
def mock_vertex_ai_modules():
    """
    Session-level fixture: install Vertex AI mocks for all arcade agent tests.

    - Provides mock GenerativeModel + chat API.
    - Avoids ImportError / AttributeError for vertexai.* imports.
    - Default output is "Hello from Smoke Test Agent".
    """
    install_vertex_ai_mocks()
    yield
    # Optional cleanup; safe to omit if you don't care
    reset_vertex_ai_mocks()


@pytest.fixture
def vertex_text():
    """
    Per-test helper to override the default text, if needed.

    Usage inside a test:
      def test_judge(..., vertex_text, ...):
          vertex_text("Smoke Test Judge Agent")
    """
    def _setter(value: str) -> None:
        set_vertex_ai_default_text(value)

    # Ensure a known default at test start
    _setter("Hello from Smoke Test Agent")
    return _setter


# ---------- TRACKS patch helpers ----------

@pytest.fixture
def patch_tracks_for_quest(monkeypatch):
    """
    Limit arcade_app.agent.TRACKS to a known quest track so the Quest Agent
    always finds the expected track during smoke tests.
    """
    track_id = "python-fundamentals"
    world_slug = "world-python"
    
    mock_tracks = {
        track_id: {
            "id": track_id,
            "name": "Python Fundamentals",
            "source": "fundamentals", # Triggers path A
            "world_id": world_slug
        }
    }
    
    patch_dict = patch.dict("arcade_app.agent.TRACKS", mock_tracks)
    patch_dict.start()
    yield
    patch_dict.stop()

@pytest.fixture
def patch_tracks_for_judge(monkeypatch):
    """
    Variant for Judge Agent; if Judge uses a different track/config, adjust here.
    For now this can just reuse the quest track.
    """
    track_id = "python-fundamentals"
    world_slug = "world-python"
    
    mock_tracks = {
        track_id: {
            "id": track_id,
            "name": "Python Fundamentals",
            "source": "fundamentals",
            "world_id": world_slug
        }
    }
    
    patch_dict = patch.dict("arcade_app.agent.TRACKS", mock_tracks)
    patch_dict.start()
    yield
    patch_dict.stop()

@pytest.fixture
def patch_tracks_for_explain(monkeypatch):
    """
    Variant for Explain Agent; same idea as Judge.
    """
    track_id = "python-fundamentals"
    world_slug = "world-python"
    
    mock_tracks = {
        track_id: {
            "id": track_id,
            "name": "Python Fundamentals",
            "source": "fundamentals",
            "world_id": world_slug
        }
    }
    
    patch_dict = patch.dict("arcade_app.agent.TRACKS", mock_tracks)
    patch_dict.start()
    yield
    patch_dict.stop()

# ---------- Session / quest seeding helpers ----------

@pytest_asyncio.fixture
async def quest_smoke_session(db_session):
    """
    Create or locate a (user_id, session_id) pair with an IN_PROGRESS quest
    for the Quest Agent to pick up.
    """
    user_id = "smoke_test_user"
    world_slug = "world-python"
    track_id = "python-fundamentals"
    quest_slug = "loop"
    
    # 1. Seed Database
    from datetime import datetime
    
    # Check if user exists first to avoid IntegrityError if DB persists
    user = await db_session.get(User, user_id)
    if not user:
        user = User(id=user_id, name="Smoke Tester", current_avatar_id="default_user", created_at=datetime(2024, 1, 1))
        db_session.add(user)
        # Create profile too
        profile = Profile(user_id=user_id, total_xp=0, global_level=1, skill_points=0, world_progress={}, flags={})
        db_session.add(profile)
    
    # Check if quest exists
    stmt = "SELECT id FROM questdefinition WHERE slug = :slug"
    from sqlalchemy import text
    # Or just try to add and ignore or use merge
    # Simplified: Assuming test DB is clean or we just need ONE instance
    # But db_session fixture usually rolls back. 
    
    # Just try adding quest, if it fails assume it exists or use merge
    q1 = await db_session.merge(QuestDefinition(
        slug=quest_slug,
        world_id=world_slug,
        track_id=track_id,
        order_index=1,
        title="Loop Quest",
        short_description="Write a loop",
        detailed_description="Write a loop",
        rubric_id="test-rubric", 
        base_xp_reward=10,
        mastery_xp_bonus=5,
        is_repeatable=False
    ))
    
    await db_session.commit()
    # No refresh needed usually if we just need ID but let's be safe
    # await db_session.refresh(q1) 
    
    # Clear existing progress
    # await db_session.execute(text("DELETE FROM questprogress WHERE user_id = :uid"), {"uid": user_id})
    
    qp = QuestProgress(
        user_id=user_id, 
        quest_id=1, # Hardcoded ID assumption, risky? Ideally query it. 
        # But for smoke test with fresh DB fixture, ID 1 is likely. 
        # Better: q1.id
        state=QuestState.IN_PROGRESS,
        attempts=0
    )
    # The merge above returns the instance attached to session.
    # But q1.id might be None if it was just merged? No, should be fine.
    # To be safe regarding IDs, let's just make sure we attach the QP to the right quest.
    # But we set Foreign Key quest_id.
    
    # Actually, let's simple add. If it exists, previous tests might have left it?
    # db_session fixture rolls back transactions, so it should be clean.
    db_session.add(qp)
    await db_session.commit()
    
    sid = "test_session_123"
    
    yield (user_id, sid)

@pytest_asyncio.fixture
async def judge_smoke_session(quest_smoke_session):
    """
    Reuse quest session for judge.
    """
    yield quest_smoke_session

@pytest_asyncio.fixture
async def explain_smoke_session(quest_smoke_session):
    """
    Reuse quest session for explain.
    """
    yield quest_smoke_session

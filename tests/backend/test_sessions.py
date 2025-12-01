import pytest
import json
from sqlmodel import select
from arcade_app.models import User, ChatSession
from arcade_app.session_helper import get_or_create_session, update_session_state, append_message
from fastapi.testclient import TestClient
from arcade_app.agent import app
from unittest.mock import patch

# Mark all async tests
pytestmark = pytest.mark.asyncio

@pytest.fixture
async def session_setup(db_session):
    """Seeds a user for session testing."""
    user = User(id="player1", name="Player One")
    db_session.add(user)
    await db_session.commit()

async def test_create_new_session(db_session, session_setup):
    """Verify a new session is created if none exists."""
    # 1. Helper Call
    data = await get_or_create_session("player1")
    
    assert data["user_id"] == "player1"
    assert data["history"] == []
    # Check defaults
    assert data["world_id"] == "world-python"
    
    # 2. Verify DB
    session = (await db_session.execute(select(ChatSession).where(ChatSession.user_id == "player1"))).scalars().first()
    assert session is not None

async def test_resume_existing_session(db_session, session_setup):
    """Verify we get the same session back if we call it again."""
    # 1. Create first session
    first = await get_or_create_session("player1")
    
    # 2. Call again
    second = await get_or_create_session("player1")
    
    assert first["id"] == second["id"]
    
    # 3. Verify count is still 1
    sessions = (await db_session.execute(select(ChatSession))).scalars().all()
    assert len(sessions) == 1

async def test_update_context(db_session, session_setup):
    """Verify we can change the user's cursor position (World/Track)."""
    # Setup
    data = await get_or_create_session("player1")
    sid = data["id"]
    
    # Update
    new_context = {"world_id": "world-infra", "mode": "debug"}
    await update_session_state(sid, new_context)
    
    # Verify DB
    # Force expire to ensure fresh read
    db_session.expire_all()
    session = await db_session.get(ChatSession, sid)
    
    assert session.world_id == "world-infra"
    assert session.mode == "debug"
    # Track ID should remain unchanged (default)
    assert session.track_id == "applylens-backend"

async def test_message_logging(db_session, session_setup):
    """Verify chat history persists."""
    data = await get_or_create_session("player1")
    sid = data["id"]
    
    # 1. Add User Message
    await append_message(sid, "user", "Hello System")
    
    # 2. Add Assistant Message with Meta
    await append_message(sid, "assistant", "Hello User", meta={"npc": "KAI"})
    
    # 3. Verify
    db_session.expire_all()
    session = await db_session.get(ChatSession, sid)
    
    history = session.history
    assert len(history) == 2
    
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello System"
    
    assert history[1]["role"] == "assistant"
    assert history[1]["npc"] == "KAI"
    assert "timestamp" in history[1]

async def test_api_restore_session(db_session, session_setup):
    """Verify the API endpoint returns the session for the logged-in user."""
    client = TestClient(app)
    
    # Pre-seed a session with custom state
    sid = (await get_or_create_session("player1"))["id"]
    await update_session_state(sid, {"world_id": "world-test"})
    
    # Mock Auth to be 'player1'
    async def mock_get_user():
        return {"id": "player1"}

    with patch("arcade_app.agent.get_current_user", side_effect=mock_get_user):
        response = client.get("/api/session/active")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sid
        assert data["world_id"] == "world-test"

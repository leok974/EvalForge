import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from arcade_app.agent import app, AGENTS

client = TestClient(app)

@pytest.mark.asyncio
async def test_stream_session_passes_codex_id(monkeypatch):
    """
    Verify that the stream_session endpoint correctly extracts codex_id 
    from the payload and passes it to the agent's run method context.
    """
    
    # 1. Mock Auth & Session Helpers
    async def fake_get_current_user(request):
        return {"id": "test-user"}
    
    async def fake_get_or_create_session(user_id):
        return {"id": "test-session"}
        
    async def fake_update_session_state(sid, state):
        pass
        
    async def fake_append_message(sid, role, content):
        pass

    monkeypatch.setattr("arcade_app.agent.get_current_user", fake_get_current_user)
    monkeypatch.setattr("arcade_app.agent.get_or_create_session", fake_get_or_create_session)
    monkeypatch.setattr("arcade_app.agent.update_session_state", fake_update_session_state)
    monkeypatch.setattr("arcade_app.agent.append_message", fake_append_message)

    # 2. Mock the ExplainAgent
    mock_agent = MagicMock()
    # run must return an async generator
    async def fake_run(user_input, context):
        yield {"event": "text_delta", "data": f"Context codex_id: {context.get('codex_id')}"}
        yield {"event": "done", "data": "[DONE]"}
    
    mock_agent.run = fake_run
    
    # Replace the real explain agent in the registry
    original_agent = AGENTS.get("explain")
    AGENTS["explain"] = mock_agent
    
    try:
        # 3. Make the Request
        response = client.post(
            "/apps/arcade_app/users/test-user/sessions/test-session/query/stream",
            json={
                "message": "Help me!",
                "mode": "explain",
                "world_id": "world-1",
                "track_id": "track-1",
                "codex_id": "boss-strategy-123"  # <--- The key field we are testing
            }
        )
        
        # 4. Verify Response
        assert response.status_code == 200
        content = response.text
        
        # Check if the mock agent echoed the codex_id
        assert "Context codex_id: boss-strategy-123" in content
        
    finally:
        # Restore original agent
        if original_agent:
            AGENTS["explain"] = original_agent

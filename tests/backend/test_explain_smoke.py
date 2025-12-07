import pytest
from unittest.mock import patch, AsyncMock
from httpx import AsyncClient
from arcade_app.agent import app

pytestmark = pytest.mark.asyncio

async def test_explain_agent_smoke_sse(
    client: AsyncClient,
    db_session, 
    mock_vertex_ai_modules, 
    patch_tracks_for_explain, 
    explain_smoke_session,
    vertex_text
):
    """
    Smoke test for Explain Agent.
    """
    vertex_text("Hello from Smoke Test Agent")

    user_id, sid = explain_smoke_session
    world_slug = "world-python"
    track_id = "python-fundamentals"
    
    async def mock_get_session():
        yield db_session

    # We mock get_chat_model because LangChain's ChatVertexAI validation 
    # might still try to auth even with vertexai mocked, or fail on other internals.
    # But let's try to pass through to our simple mock if possible.
    # For safety in this "Clean Refactor" step, I will map the mock_llm to respond 
    # with the text set by vertex_text() to keep consistency.
    
    msg_mock = AsyncMock()
    msg_mock.content = "Hello from Smoke Test Agent"
    
    async def mock_astream(messages):
        yield msg_mock
        
    mock_llm = AsyncMock()
    mock_llm.astream.side_effect = mock_astream

    with patch("arcade_app.quest_helper.get_session", side_effect=mock_get_session), \
         patch("arcade_app.session_helper.get_session", side_effect=mock_get_session), \
         patch("arcade_app.explain_agent.get_session", side_effect=mock_get_session), \
         patch("arcade_app.llm.get_chat_model", return_value=mock_llm):
         
        url = f"/apps/arcade_app/users/{user_id}/sessions/{sid}/query/stream"
        
        payload = {
            "message": "Explain loops",
            "mode": "explain",
            "world_id": world_slug,
            "track_id": track_id
        }
        
        async with client.stream("POST", url, json=payload) as response:
            assert response.status_code == 200
            
            content = ""
            async for line in response.aiter_lines():
                content += line
            
            # Check for text_delta
            assert "event: text_delta" in content
            assert "Hello from Smoke Test Agent" in content

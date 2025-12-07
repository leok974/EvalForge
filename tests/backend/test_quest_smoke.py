import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_quest_agent_smoke_streams_response(
    client: AsyncClient,
    mock_vertex_ai_modules,
    patch_tracks_for_quest,
    quest_smoke_session,
    vertex_text,
):
    """
    1. Resets any previous mocks.
    2. Calls the streaming endpoint.
    3. Verifies we get chunks back (status 200 + 'text_delta').
    """
    # Optional: set explicit text for clarity (can be same as default)
    vertex_text("Hello from Smoke Test Agent")

    user_id, session_id = quest_smoke_session
    url = f"/apps/arcade_app/users/{user_id}/sessions/{session_id}/query/stream"

    # Send a message to trigger the agent
    payload = {
        "message": "Start the Quest",
        "mode": "quest",
        "world_id": "world-python",
        "track_id": "python-fundamentals"
    }

    # Use httpx's async client stream
    async with client.stream("POST", url, json=payload) as response:
        assert response.status_code == 200
        
        # We just want to see *some* data coming back
        # The first few events might be 'npc_identity' or 'status'
        # Eventually we want 'text_delta'
        
        found_text = False
        async for line in response.aiter_lines():
            print(f"DEBUG STREAM LINE: {line!r}")
            if "event: text_delta" in line:
                found_text = True
            
            # Additional check for the content
            if "Hello from Smoke Test Agent" in line:
                found_text = True
                break
        
        assert found_text, "Stream did not return any text_delta events"

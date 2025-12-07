import pytest
from unittest.mock import patch, AsyncMock
from httpx import AsyncClient
from arcade_app.agent import app

pytestmark = pytest.mark.asyncio

async def test_judge_agent_smoke_sse(
    client: AsyncClient,
    db_session, 
    mock_vertex_ai_modules, 
    patch_tracks_for_judge, 
    judge_smoke_session,
    vertex_text
):
    """
    Smoke test for Judge Agent. 
    Verifies it receives JSON grade from mocked LLM and streams feedback.
    """
    import json
    
    # Judge checks for JSON strict format
    mock_grade = json.dumps({
        "coverage": 5,
        "correctness": 5,
        "clarity": 5,
        "comment": "Excellent work!",
        "weighted_score": 100
    })
    vertex_text(mock_grade)

    user_id, sid = judge_smoke_session
    world_slug = "world-python"
    track_id = "python-fundamentals"
    
    async def mock_get_session():
        yield db_session

    # Maintain DB/Gamification patches
    with patch("arcade_app.quest_helper.get_session", side_effect=mock_get_session), \
         patch("arcade_app.session_helper.get_session", side_effect=mock_get_session), \
         patch("arcade_app.database.get_session", side_effect=mock_get_session), \
         patch("arcade_app.gamification.add_xp", new_callable=AsyncMock) as mock_xp, \
         patch("arcade_app.gamification.process_quest_completion", new_callable=AsyncMock) as mock_complete_global, \
         patch("arcade_app.agent.process_quest_completion", new_callable=AsyncMock) as mock_complete_agent:
         
        mock_xp.return_value = {"level": 1, "xp": 10}
         
        url = f"/apps/arcade_app/users/{user_id}/sessions/{sid}/query/stream"
        
        payload = {
            "message": "print('hello')",
            "mode": "judge", 
            "world_id": world_slug,
            "track_id": track_id
        }
        
        async with client.stream("POST", url, json=payload) as response:
            assert response.status_code == 200
            
            content = ""
            async for line in response.aiter_lines():
                content += line
                
            # Check for generic success indicators
            # The agent might stream text or event: grade
            assert "event: text_delta" in content or "event: grade" in content
            
            # If our mock worked, we might see the JSON text streamed back too
            # (since stream_coach_feedback uses the same mock response)
            assert "Excellent work!" in content

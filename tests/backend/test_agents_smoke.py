
import pytest
import os
import json
import asyncio
from unittest.mock import MagicMock, patch
from arcade_app.agent import AGENTS
from tests.backend.vertex_ai_mocks import install_vertex_ai_mocks, reset_vertex_ai_mocks, set_vertex_ai_default_text

@pytest.fixture(scope="function", autouse=True)
def mock_vertex_ai_env():
    """Install Vertex AI mocks before each test and clean up after."""
    install_vertex_ai_mocks()
    yield
    reset_vertex_ai_mocks()

@pytest.mark.asyncio
async def test_judge_agent_smoke_streams_response(
    client,
    mock_vertex_ai_modules,
    patch_tracks_for_judge,
    judge_smoke_session,
    vertex_text,
):
    """
    Verify JudgeAgent runs and streams chunks via the API.
    """
    vertex_text('{"coverage": 5, "correctness": 5, "clarity": 5, "comment": "Mocked Judge Decision"}')
    
    user_id, session_id = judge_smoke_session
    # Updated URL to match new endpoint
    url = "/api/agent/query/stream"
    
    payload = {
        "message": "Evaluate this code.",
        "mode": "judge",
        "world_id": "world-python",
        "track_id": "python-fundamentals"
    }

    async with client.stream("POST", url, json=payload) as response:
        assert response.status_code == 200
        
        found_text = False
        async for line in response.aiter_lines():
            if "event: text_delta" in line:
                found_text = True
            if "Mocked Judge Decision" in line:
                found_text = True
            # Also check for grade event payload if possible, but text_delta usually carries the comment explanation?
            # JudgeAgent streams "grade" event heavily.
            if "event: grade" in line:
                found_text = True
            if "event: text_delta" in line:
                # Judge might stream feedback text if "stream_coach_feedback" is called.
                found_text = True
        
        assert found_text, "Judge agent did not return any text_delta events"


@pytest.mark.asyncio
async def test_explain_agent_smoke_streams_response(
    client,
    mock_vertex_ai_modules,
    patch_tracks_for_explain,
    explain_smoke_session,
    vertex_text,
):
    """
    Verify ExplainAgent runs and streams chunks via the API.
    """
    vertex_text("Mocked Explanation")
    
    user_id, session_id = explain_smoke_session
    url = "/api/agent/query/stream"
    
    payload = {
        "message": "Explain this concept.",
        "mode": "explain",
        "world_id": "world-python",
        "track_id": "python-fundamentals"
    }

    async with client.stream("POST", url, json=payload) as response:
        assert response.status_code == 200
        
        found_text = False
        async for line in response.aiter_lines():
            if "event: text_delta" in line:
                found_text = True
            if "Mocked Explanation" in line:
                found_text = True
        
        assert found_text, "Explain agent did not return any text_delta events"

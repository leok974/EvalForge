import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from arcade_app.agent import app
from arcade_app.onboarding_helper import stream_prologue

# Mark async tests
pytestmark = pytest.mark.asyncio

# --- TEST 1: The Narrative Script (Unit Test) ---
async def test_prologue_script_content():
    """Verify the helper yields the correct cinematic lines."""
    
    # Patch sleep to run instantly
    with patch("asyncio.sleep", return_value=None):
        chunks = []
        async for chunk in stream_prologue("test_user"):
            chunks.append(chunk)
            
        full_text = "".join(chunks)
        
        # Check for key beats
        assert "INITIALIZING NEURO-LINK" in full_text
        assert "Wake up, Architect" in full_text
        assert "MISSION: INITIALIZE" in full_text
        assert "Sync a GitHub Repository" in full_text

# --- TEST 2: The Routing Logic (Integration Test) ---
async def test_routing_intercepts_new_user():
    """Verify that a 0 XP user gets the prologue when typing 'start'."""
    client = TestClient(app)
    
    # 1. Mock Profile (0 XP)
    mock_profile = {"total_xp": 0, "level": 1}
    
    # 2. Patch dependencies
    # Patch get_profile to return our noob user
    # Patch asyncio.sleep to skip animation delays
    with patch("arcade_app.agent.get_profile", new_callable=AsyncMock) as mock_get_profile, \
         patch("arcade_app.onboarding_helper.asyncio.sleep", return_value=None):
        
        mock_get_profile.return_value = mock_profile
        
        # 3. Make Request
        response = client.post(
            "/apps/arcade_app/users/noob/sessions/s1/query/stream",
            json={
                "message": "start", 
                "mode": "quest", 
                "world_id": "world-python",
                "track_id": "track-1"
            }
        )
        
        # 4. Verify Response
        # The SSE stream should contain the prologue text
        content = response.text
        assert "SYSTEM BOOT SEQUENCE" in content
        assert "INITIALIZING NEURO-LINK" in content

async def test_routing_allows_veteran_user():
    """Verify that a >0 XP user goes to the normal Agent."""
    client = TestClient(app)
    
    # 1. Mock Profile (100 XP)
    mock_profile = {"total_xp": 100, "level": 1}
    
    # 2. Mock the Normal Agent (QuestAgent)
    # We want to ensure the router calls AGENT.run(), not stream_prologue
    mock_agent_run = AsyncMock()
    # Mock the generator return value properly
    async def mock_gen(*args, **kwargs):
        yield {"event": "text_delta", "data": "Normal Quest"}
    mock_agent_run.side_effect = mock_gen
    
    with patch("arcade_app.agent.get_profile", new_callable=AsyncMock) as mock_get_profile, \
         patch("arcade_app.agent.AGENTS") as mock_agents:
        
        mock_get_profile.return_value = mock_profile
        
        # Setup the mock agent registry to return our mock
        mock_agent_instance = MagicMock()
        mock_agent_instance.run = mock_agent_run
        mock_agents.get.return_value = mock_agent_instance
        
        # 3. Make Request
        client.post(
            "/apps/arcade_app/users/vet/sessions/s1/query/stream",
            json={"message": "start", "mode": "quest"}
        )
        
        # 4. Verify
        # The prologue string should NOT be in the output (handled by mock agent)
        # Verify the agent's run method was called
        mock_agent_run.assert_called_once()

import pytest
import json
import os
from unittest.mock import AsyncMock, patch, MagicMock
from arcade_app.persona_helper import get_npc, wrap_prompt_with_persona
from arcade_app.agent import ExplainAgent

# Mark async tests
pytestmark = pytest.mark.asyncio

def test_npc_data_integrity():
    """Verify npcs.json is valid and contains core roles."""
    # Ensure file exists
    assert os.path.exists("data/npcs.json")
    
    # Check specific keys
    kai = get_npc("quest")
    assert kai["name"] == "KAI"
    assert kai["role"] == "quest"
    
    elara = get_npc("explain")
    assert elara["name"] == "ELARA"
    assert "Archivist" in elara["title"]

def test_prompt_wrapping():
    """Verify the helper injects the voice prompt."""
    base = "Explain FastAPI."
    wrapped = wrap_prompt_with_persona(base, "debug")
    
    # Check for PATCH's specific traits
    patch_npc = get_npc("debug")
    assert patch_npc["voice_prompt"] in wrapped
    assert "IDENTITY PROTOCOL" in wrapped
    assert "TASK:\n    Explain FastAPI." in wrapped

async def test_agent_emits_identity_event():
    """Verify that an Agent emits the 'npc_identity' event first."""
    agent = ExplainAgent()
    context = {"track_id": "track-1"}
    
    # Mock the graph execution so we don't hit Vertex AI
    # We only care about the *first* yield which happens before the graph starts
    with patch("arcade_app.agent.wrap_prompt_with_persona") as mock_wrap, \
         patch("arcade_app.graph_agent.explain_graph") as mock_graph:
        
        # Mock graph stream to yield nothing/done immediately
        async def empty_stream(*args, **kwargs):
            yield {"event": "on_chat_model_stream", "data": {"chunk": MagicMock(content="Done")}}
            
        mock_graph.astream_events.side_effect = empty_stream
        
        # Collect events
        events = []
        async for event in agent.run("Test", context):
            events.append(event)
            
        # Assertion: First event must be identity
        first_event = events[0]
        assert first_event["event"] == "npc_identity"
        
        data = json.loads(first_event["data"])
        assert data["name"] == "ELARA"
        assert data["role"] == "explain"

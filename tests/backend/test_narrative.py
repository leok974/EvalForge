import json
import pytest
import os
from unittest.mock import AsyncMock, MagicMock, patch
from arcade_app.quest_helper import stream_quest_generator

# Mark all async tests
pytestmark = pytest.mark.asyncio

def test_worlds_data_integrity():
    """Verify worlds.json has the required narrative config."""
    # This test reads the ACTUAL file on disk to ensure no typos in the JSON
    worlds_path = "data/worlds.json"
    assert os.path.exists(worlds_path), "worlds.json missing!"
    
    with open(worlds_path, "r", encoding="utf-8") as f:
        worlds = json.load(f)
    
    # Check Python World specifically (since we rely on it for defaults)
    py_world = next((w for w in worlds if w["id"] == "world-python"), None)
    assert py_world is not None
    
    config = py_world.get("narrative_config", {})
    assert config.get("alias") == "THE FOUNDRY"
    assert "industrial" in config.get("theme", "").lower()
    assert len(config.get("vocabulary", [])) > 0

async def test_narrative_prompt_injection():
    """Verify that the quest generator injects the narrative persona into the LLM prompt."""
    
    # 1. Setup Mock Track & World Context
    track_context = {
        "name": "Test Track",
        "world_id": "world-python", # Should trigger 'THE FOUNDRY'
        "description": "Testing things",
        "tags": ["test"],
        "source": "fundamentals"
    }

    # 2. Mock Vertex AI
    mock_model = MagicMock()
    mock_response = AsyncMock()
    mock_response.__aiter__.return_value = [MagicMock(text="Quest Content")]
    mock_model.generate_content_async = AsyncMock(return_value=mock_response)

    # Patch vertexai.init and GenerativeModel since they are imported inside the function
    with patch("vertexai.init"), \
         patch("vertexai.generative_models.GenerativeModel", return_value=mock_model):
        
        # 3. Run the Helper
        # We need to consume the generator to trigger execution
        async for _ in stream_quest_generator("start", track_context):
            pass
            
        # 4. Verify the Prompt
        # Extract the prompt string passed to generate_content_async
        call_args = mock_model.generate_content_async.call_args
        prompt_sent = call_args[0][0]
        
        # Assertions: Did the narrative get injected?
        assert "ROLE: You are a Automation Engineer" in prompt_sent
        assert "THEME: Industrial Clockwork" in prompt_sent
        assert "INCOMING TRANSMISSION: THE FOUNDRY" in prompt_sent
        assert "VOCABULARY TO USE: gear, cycle" in prompt_sent

async def test_narrative_fallback():
    """Verify it falls back gracefully if world ID is unknown."""
    track_context = {
        "name": "Unknown Track",
        "world_id": "world-void", 
        "source": "fundamentals"
    }

    mock_model = MagicMock()
    mock_model.generate_content_async = AsyncMock(return_value=AsyncMock())

    with patch("vertexai.init"), \
         patch("vertexai.generative_models.GenerativeModel", return_value=mock_model):
        async for _ in stream_quest_generator("start", track_context):
            pass
            
        prompt_sent = mock_model.generate_content_async.call_args[0][0]
        
        # Should use defaults from code (THE SYSTEM / Engineer)
        assert "INCOMING TRANSMISSION: THE SYSTEM" in prompt_sent

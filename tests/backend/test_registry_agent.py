import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock
from langchain_core.messages import AIMessageChunk
from arcade_app.agent import QuestAgent

# Mark async tests
pytestmark = pytest.mark.asyncio

async def test_registry_routing_logic():
    """
    Verify QuestAgent routes to the Graph when track_id is 'project-registry'.
    """
    agent = QuestAgent()
    context = {"track_id": "project-registry", "user_id": "commander"}
    
    # 1. Define Mock Graph Events
    # Simulating: Tool Start -> Tool End (Implicit) -> Final Text
    mock_events = [
        {
            "event": "on_tool_start",
            "name": "list_my_projects",
            "data": {}
        },
        {
            "event": "on_chat_model_stream",
            "data": {"chunk": AIMessageChunk(content="Here are your")}
        },
        {
            "event": "on_chat_model_stream",
            "data": {"chunk": AIMessageChunk(content=" projects.")}
        }
    ]

    # Generator for the mock stream
    async def mock_stream(*args, **kwargs):
        for e in mock_events:
            yield e

    # 2. Patch dependencies
    # We patch the 'quest_graph' where it is defined, because it is imported locally
    with patch("arcade_app.quest_agent_graph.quest_graph") as mock_graph, \
         patch("arcade_app.agent.get_npc") as mock_npc:
        
        mock_graph.astream_events.side_effect = mock_stream
        mock_npc.return_value = {"name": "KAI", "role": "quest"}
        
        # 3. Run Agent
        results = []
        async for event in agent.run("List projects", context):
            results.append(event)
            
        # 4. Assertions
        
        # Identity First
        assert results[0]["event"] == "npc_identity"
        
        # Tool Status
        status_events = [e for e in results if e["event"] == "status"]
        assert len(status_events) > 0
        assert "Executing Protocol: list_my_projects" in status_events[0]["data"]
        
        # Text Stream
        text_events = [e for e in results if e["event"] == "text_delta"]
        full_text = "".join([e["data"] for e in text_events])
        assert "Here are your projects." in full_text
        
        # Verify Graph Input
        # Ensure we passed the system prompt with user_id
        call_args = mock_graph.astream_events.call_args
        inputs = call_args[0][0]
        assert "PROJECT REGISTRY" in inputs["messages"][0].content
        # The prompt uses single quotes for the key: 'user_id'="{user_id}"
        assert "'user_id'=\"commander\"" in inputs["messages"][0].content

async def test_standard_quest_fallback():
    """
    Verify that non-registry tracks still use the standard generator.
    """
    agent = QuestAgent()
    context = {"track_id": "python-fundamentals", "user_id": "student"}
    
    # Create an async generator for the mock
    async def mock_async_gen(*args, **kwargs):
        if False: yield # make it a generator
        return

    with patch("arcade_app.agent.stream_quest_generator", side_effect=mock_async_gen) as mock_gen, \
         patch("arcade_app.agent.get_npc") as mock_npc:
        
        mock_npc.return_value = {"name": "KAI", "role": "quest"}
        
        async for _ in agent.run("Start", context):
            pass
            
        # Should call the standard helper, NOT the graph
        mock_gen.assert_called_once()

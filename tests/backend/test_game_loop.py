import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from arcade_app.agent import app
from arcade_app.worker import spawn_boss

# Mark all async tests
pytestmark = pytest.mark.asyncio

# --- TEST 1: The Background Worker ---
async def test_spawn_boss_publishes_event():
    """
    Verifies that the worker logic publishes a valid JSON event to Redis
    when the random check passes.
    """
    # 1. Force Random to succeed (return < 0.1)
    # Patching where it is USED, not where it is defined
    with patch("arcade_app.worker.random.random", return_value=0.05):
        
        # 2. Mock Redis Connection
        mock_redis = AsyncMock()
        
        # Patch the Redis constructor
        with patch("arcade_app.worker.Redis", return_value=mock_redis):
            
            # 3. Run Worker Function
            await spawn_boss({})
            
            # 4. Verify Publish Call
            mock_redis.publish.assert_called_once()
            
            # Check Payload structure
            channel, message = mock_redis.publish.call_args[0]
            assert channel == "game_events"
            
            data = json.loads(message)
            assert data["type"] == "boss_spawn"
            assert data["xp_bounty"] == 500

async def test_spawn_boss_skips_randomly():
    """Verifies that the worker does nothing if the dice roll fails."""
    # Force Random to fail (return > 0.1)
    with patch("arcade_app.worker.random.random", return_value=0.5):
        mock_redis = AsyncMock()
        
        with patch("arcade_app.worker.Redis", return_value=mock_redis):
            await spawn_boss({})
            
            # Should NOT connect or publish
            mock_redis.publish.assert_not_called()

# --- TEST 2: The WebSocket Endpoint (FIXED) ---
async def test_websocket_broadcast():
    """
    Verifies the WebSocket endpoint receives data from Redis and sends it to the client.
    """
    client = TestClient(app)
    
    # 1. Define the mock Redis message
    # Redis library returns bytes for data
    mock_event = {
        "type": "message",
        "data": b'{"type": "boss_spawn", "title": "TEST"}'
    }

    # 2. Mock the PubSub iterator
    # CRITICAL FIX: Make it yield once then STOP (return), breaking the infinite loop
    async def mock_listen():
        yield mock_event
        return 

    mock_redis = MagicMock()
    mock_pubsub = MagicMock()
    mock_pubsub.subscribe = AsyncMock()
    # Assign our finite generator to the listen method
    mock_pubsub.listen = mock_listen
    
    mock_redis.pubsub.return_value = mock_pubsub
    mock_redis.close = AsyncMock()

    # 3. Patch Redis.from_url inside socket_manager
    with patch("arcade_app.socket_manager.Redis.from_url", return_value=mock_redis):
        
        # 4. Connect via TestClient
        with client.websocket_connect("/ws/game") as websocket:
            # Receive message
            data = websocket.receive_text()
            event = json.loads(data)
            
            assert event["type"] == "boss_spawn"
            assert event["title"] == "TEST"
            
            # The server loop finishes naturally after mock_listen returns
            # We don't need to force disconnect

import os
from fastapi import WebSocket
from redis.asyncio import Redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Create a dedicated Redis connection for this socket (Pub/Sub requires it)
    redis = Redis.from_url(REDIS_URL)
    pubsub = redis.pubsub()
    await pubsub.subscribe("game_events")

    try:
        # Loop to forward Redis messages to WebSocket
        async for message in pubsub.listen():
            if message["type"] == "message":
                # Raw bytes -> Decode -> Send to Browser
                payload = message["data"].decode("utf-8")
                await websocket.send_text(payload)
    except Exception as e:
        print(f"WebSocket disconnected: {e}")
    finally:
        await redis.close()

import json

async def emit_fx_event(user_id: str, event_data: dict):
    """
    Publishes an event to the global game_events channel.
    Frontend must filter by user_id if needed.
    """
    redis = Redis.from_url(REDIS_URL)
    try:
        payload = {
            "user_id": user_id,
            **event_data
        }
        try:
            await redis.publish("game_events", json.dumps(payload))
        except Exception as e:
            print(f"Redis publish failed (ignoring): {e}")
    finally:
        await redis.close()

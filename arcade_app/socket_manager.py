import json
import asyncio
from fastapi import WebSocket
from redis.asyncio import Redis

REDIS_URL = "redis://localhost:6379"

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

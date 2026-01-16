import os
import asyncio
import logging
from fastapi import WebSocket
from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConnectionError, RedisError
from arcade_app.config import REDIS_URL

logger = logging.getLogger(__name__)

async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time game events.
    Gracefully degrades to keep-alive mode if Redis is unavailable.
    """
    await websocket.accept()
    
    try:
        # Test Redis connection first
        redis = Redis.from_url(REDIS_URL)
        await redis.ping()  # Test connectivity
        
        # Redis is available - proceed with normal pub/sub
        logger.info("WebSocket: Redis available, enabling real-time updates")
        pubsub = redis.pubsub()
        await pubsub.subscribe("game_events")
        
        # Send confirmation to client
        await websocket.send_json({
            "type": "system",
            "status": "connected",
            "message": "Real-time updates enabled"
        })

        try:
            # Loop to forward Redis messages to WebSocket
            async for message in pubsub.listen():
                if message["type"] == "message":
                    # Raw bytes -> Decode -> Send to Browser
                    payload = message["data"].decode("utf-8")
                    await websocket.send_text(payload)
        except Exception as e:
            logger.debug(f"WebSocket disconnected during pub/sub: {e}")
        finally:
            await pubsub.unsubscribe("game_events")
            await redis.close()
            
    except (RedisConnectionError, RedisError, OSError) as e:
        # Redis unavailable - degrade gracefully
        logger.warning(f"WebSocket: Redis unavailable ({e.__class__.__name__}), running in degraded mode")
        
        try:
            # Send degraded mode notification to client
            await websocket.send_json({
                "type": "system",
                "status": "degraded",
                "message": "Real-time updates unavailable (Redis not connected). WebSocket will maintain connection for future updates."
            })
            
            # Keep connection alive but idle
            # Client can choose to poll REST API instead
            # Wait for client to close or send ping
            while True:
                try:
                    # Wait for client messages with 30s timeout
                    data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                    
                    # Handle ping/pong to keep connection alive
                    if data == "ping":
                        await websocket.send_json({"type": "pong"})
                        
                except asyncio.TimeoutError:
                    # Send keep-alive ping
                    await websocket.send_json({"type": "keep-alive"})
                    
        except Exception as e:
            logger.debug(f"WebSocket disconnected in degraded mode: {e}")
    
    except Exception as e:
        # Unexpected error
        logger.error(f"WebSocket unexpected error: {e}", exc_info=True)
        try:
            await websocket.send_json({
                "type": "error",
                "message": "WebSocket connection failed"
            })
        except:
            pass


import json

async def emit_fx_event(user_id: str, event_data: dict):
    """
    Publishes an event to the global game_events channel.
    Frontend must filter by user_id if needed.
    Gracefully handles Redis being unavailable.
    """
    try:
        redis = Redis.from_url(REDIS_URL)
        payload = {
            "user_id": user_id,
            **event_data
        }
        
        try:
            await redis.publish("game_events", json.dumps(payload))
            logger.debug(f"Published event to game_events for user {user_id}")
        except (RedisConnectionError, RedisError) as e:
            # Redis unavailable - log once at warning level
            logger.warning(f"Redis publish failed (event lost): {e.__class__.__name__}")
        except Exception as e:
            logger.error(f"Unexpected error publishing to Redis: {e}")
    except Exception as e:
        logger.error(f"Failed to create Redis client: {e}")
    finally:
        try:
            await redis.close()
        except:
            pass  # Best effort close

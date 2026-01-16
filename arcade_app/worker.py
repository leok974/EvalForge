import asyncio
import json
import random
from arq import cron
from arq.connections import RedisSettings
from redis.asyncio import Redis
from arcade_app.config import REDIS_URL

# Initialize Redis settings from centralized config
redis_settings = RedisSettings.from_dsn(REDIS_URL)

async def spawn_boss(ctx):
    """
    Cron job: Runs every minute. 10% chance to spawn a Boss.
    """
    if random.random() < 0.1: # 10% chance
        event = {
            "type": "boss_spawn",
            "title": "🚨 SYSTEM OUTAGE DETECTED",
            "message": "A critical legacy bug has surfaced in the Infra World.",
            "world_id": "world-infra",
            "xp_bounty": 500
        }
        
        # Publish to Redis Channel
        redis = Redis.from_url(REDIS_URL)
        await redis.publish("game_events", json.dumps(event))
        await redis.close()
        print(f"🔥 Boss Spawned: {event['title']}")

class WorkerSettings:
    functions = [spawn_boss]
    cron_jobs = [
        cron(spawn_boss, minute=None, second=0) # Run every minute at :00
    ]
    redis_settings = redis_settings

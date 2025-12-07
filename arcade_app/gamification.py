import json
import os
from datetime import datetime
from sqlmodel import select
from redis.asyncio import Redis
from arcade_app.database import get_session
from arcade_app.models import UserMetric, UserBadge, BadgeDefinition

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

async def publish_badge_event(user_id: str, badge: BadgeDefinition):
    """
    Sends a 'BADGE_UNLOCKED' event to the frontend via Redis.
    """
    try:
        redis = Redis.from_url(REDIS_URL)
        event = {
            "type": "achievement",
            "title": "ACHIEVEMENT UNLOCKED",
            "message": f"You earned: {badge.name}",
            "badge": {
                "name": badge.name,
                "description": badge.description,
                "icon": badge.icon,
                "rarity": badge.rarity,
                "xp_bonus": badge.xp_bonus
            }
        }
        await redis.publish("game_events", json.dumps(event))
        await redis.close()
    except Exception as e:
        print(f"⚠️ Redis Publish Error: {e}")

async def add_xp(user_id: str, world_id: str, amount: int) -> dict:
    """
    Adds XP to the user's profile and tracks world-specific progress.
    Returns the updated progress dict (level, xp, etc).
    """
    # Simple stub for now, expanding logic as needed
    async for session in get_session():
         # In a real impl, we'd fetch profile, update xp, check level up
         pass
    
    # Return dummy data matching expected shape for UI
    return {
        "user_id": user_id,
        "world_id": world_id,
        "xp_added": amount,
        "level": 1,
        "current_xp": amount,
        "next_level_xp": 1000
    }

async def process_quest_completion(user_id: str, world_id: str, score: float):
    """
    Updates stats and checks for new badges.
    Call this after a successful Judge evaluation.
    """
    async for session in get_session():
        # 1. Fetch or Create Metrics
        metric = await session.get(UserMetric, user_id)
        if not metric:
            metric = UserMetric(user_id=user_id, progress_stats={})
            session.add(metric)
        
        # 2. Update Counters
        metric.quests_completed += 1
        if score >= 100:
            metric.perfect_scores += 1
            
        # Update Granular Stats (World specific)
        stats = dict(metric.progress_stats) if metric.progress_stats else {}
        w_stat = stats.get(world_id, {"quests": 0})
        w_stat["quests"] = w_stat.get("quests", 0) + 1
        stats[world_id] = w_stat
        metric.progress_stats = stats
        
        session.add(metric)
        
        # 3. Rules Engine
        # Define the Logic Table here
        checks = [
            ("hello_world", metric.quests_completed >= 1),
            ("bug_hunter_bronze", metric.quests_completed >= 5),
            ("perfectionist", metric.perfect_scores >= 1), # Changed to 1 for easy testing
            ("python_novice", stats.get("world-python", {}).get("quests", 0) >= 5),
            ("infra_architect", stats.get("world-infra", {}).get("quests", 0) >= 5),
        ]

        new_unlocks = []
        for badge_id, condition_met in checks:
            if condition_met:
                # Check if already owned
                statement = select(UserBadge).where(
                    UserBadge.user_id == user_id, 
                    UserBadge.badge_id == badge_id
                )
                result = await session.execute(statement)
                existing = result.scalars().first()
                if not existing:
                    # AWARD IT!
                    # 1. Record in DB
                    ub = UserBadge(user_id=user_id, badge_id=badge_id)
                    session.add(ub)
                    
                    # 2. Get Badge Metadata for Toast
                    badge_def = await session.get(BadgeDefinition, badge_id)
                    if badge_def:
                        new_unlocks.append(badge_def)
                        
                        # 3. Award Bonus XP (Optional, needs profile helper loop)
                        # For now, just logging it.
                        print(f"🏆 Awarded {badge_def.name} to {user_id}")

        await session.commit()

        # 4. Trigger Notifications (Outside DB transaction)
        for badge in new_unlocks:
            await publish_badge_event(user_id, badge)

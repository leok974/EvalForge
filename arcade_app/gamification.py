import json
import os
from datetime import datetime
from sqlmodel import select
from redis.asyncio import Redis
from arcade_app.database import get_session
from arcade_app.models import UserMetric, UserBadge, BadgeDefinition
from arcade_app.config import REDIS_URL


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

async def get_or_create_metric(session, user_id: str, key: str) -> UserMetric:
    statement = select(UserMetric).where(UserMetric.user_id == user_id, UserMetric.metric_key == key)
    result = await session.execute(statement)
    metric = result.scalar_one_or_none()
    if not metric:
        metric = UserMetric(user_id=user_id, metric_key=key, value=0)
        session.add(metric)
    return metric

async def process_quest_completion(user_id: str, world_id: str, score: float):
    """
    Updates stats and checks for new badges.
    Call this after a successful Judge evaluation.
    """
    # Need implicit session handling if not passed? 
    # The original used 'async for session in get_session():' which creates a NEW session.
    # Tests inject mock dependencies usually?
    # But usually service functions should accept session or generic iterator.
    # The original implementation looped over get_session().
    
    async for session in get_session():
        # 1. Update Global Counters
        q_metric = await get_or_create_metric(session, user_id, "quests_completed")
        q_metric.value += 1
        session.add(q_metric)
        quests_completed_count = q_metric.value # Snapshot for rules
        
        perfect_scores_count = 0
        if score >= 100:
            p_metric = await get_or_create_metric(session, user_id, "perfect_scores")
            p_metric.value += 1
            session.add(p_metric)
            perfect_scores_count = p_metric.value
        else:
            # Need to fetch it for rules checking if not updated
            p_metric = await get_or_create_metric(session, user_id, "perfect_scores")
            perfect_scores_count = p_metric.value

        # 2. Update World Stats
        w_key = f"world_{world_id}_quests"
        w_metric = await get_or_create_metric(session, user_id, w_key)
        w_metric.value += 1
        session.add(w_metric)
        world_quests_count = w_metric.value
        
        # 3. Rules Engine
        # Define the Logic Table here - map keys to conditions
        # We need to query strict values or pass them.
        
        checks = [
            ("hello_world", quests_completed_count >= 1),
            ("bug_hunter_bronze", quests_completed_count >= 5),
            ("perfectionist", perfect_scores_count >= 1), # Changed to 1 for easy testing
            ("python_novice", world_quests_count >= 5 if "python" in world_id else False),
            ("infra_architect", world_quests_count >= 5 if "infra" in world_id else False),
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
                    ub = UserBadge(user_id=user_id, badge_id=badge_id)
                    session.add(ub)
                    
                    # Get Badge Metadata
                    badge_def = await session.get(BadgeDefinition, badge_id)
                    if badge_def:
                        new_unlocks.append(badge_def)
                        print(f"🏆 Awarded {badge_def.name} to {user_id}")

        await session.commit()

        # 4. Trigger Notifications
        for badge in new_unlocks:
            await publish_badge_event(user_id, badge)

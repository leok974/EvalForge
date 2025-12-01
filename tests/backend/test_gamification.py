import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from sqlmodel import select
from arcade_app.models import User, UserMetric, UserBadge, BadgeDefinition
from arcade_app.gamification import process_quest_completion

# Mark all async tests
pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture
async def seed_badges(db_session):
    """Pre-load the badge definitions needed for logic."""
    badges = [
        BadgeDefinition(id="hello_world", name="Hello", description="First Quest", icon="👋", rarity="common", xp_bonus=50, category="general"),
        BadgeDefinition(id="bug_hunter_bronze", name="Hunter", description="5 Quests", icon="🐛", rarity="common", xp_bonus=100, category="general")
    ]
    for b in badges:
        db_session.add(b)
    await db_session.commit()

async def test_award_first_badge(db_session, seed_badges):
    # 1. Setup User
    user = User(id="gamer", name="Gamer")
    db_session.add(user)
    await db_session.commit()

    # 2. Mock Redis (to verify notification)
    mock_redis = AsyncMock()
    mock_redis.publish = AsyncMock()
    mock_redis.close = AsyncMock()

    with patch("arcade_app.gamification.Redis.from_url", return_value=mock_redis):
        
        # 3. Complete 1st Quest (Should trigger 'hello_world')
        # World doesn't matter for this generic badge
        await process_quest_completion("gamer", "world-python", 80)
        
        # 4. Verify DB State
        # Metrics should update
        metric = await db_session.get(UserMetric, "gamer")
        assert metric.quests_completed == 1
        
        # Badge should exist
        result = await db_session.execute(select(UserBadge).where(UserBadge.user_id == "gamer"))
        badges = result.scalars().all()
        assert len(badges) == 1
        assert badges[0].badge_id == "hello_world"
        
        # 5. Verify Notification
        mock_redis.publish.assert_called_once()
        call_args = mock_redis.publish.call_args[0]
        assert "ACHIEVEMENT UNLOCKED" in call_args[1]

async def test_idempotency_no_duplicate_badges(db_session, seed_badges):
    # 1. Setup User who ALREADY has the badge
    user = User(id="veteran", name="Veteran")
    metric = UserMetric(user_id="veteran", quests_completed=1)
    existing_badge = UserBadge(user_id="veteran", badge_id="hello_world")
    
    db_session.add(user)
    db_session.add(metric)
    db_session.add(existing_badge)
    await db_session.commit()

    # 2. Mock Redis
    mock_redis = AsyncMock()
    
    with patch("arcade_app.gamification.Redis.from_url", return_value=mock_redis):
        
        # 3. Complete 2nd Quest (Total 2)
        # 'hello_world' condition (>=1) is met, but should NOT award again
        await process_quest_completion("veteran", "world-python", 80)
        
        # 4. Verify DB State
        # Metric updated to 2
        await db_session.refresh(metric)
        assert metric.quests_completed == 2
        
        # Badge count should still be 1
        result = await db_session.execute(select(UserBadge).where(UserBadge.user_id == "veteran"))
        badges = result.scalars().all()
        assert len(badges) == 1
        
        # 5. Verify Notification NOT sent
        mock_redis.publish.assert_not_called()

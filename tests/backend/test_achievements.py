import pytest
from unittest.mock import AsyncMock, patch
from sqlmodel import select
from arcade_app.models import User, UserMetric, UserBadge, BadgeDefinition
from arcade_app.gamification import process_quest_completion

# Mark all async tests
pytestmark = pytest.mark.asyncio

@pytest.fixture
async def achievement_setup(db_session):
    """Seeds the DB with badge definitions."""
    badges = [
        BadgeDefinition(id="hello_world", name="Hello", description="1 Quest", rarity="common", xp_bonus=50),
        BadgeDefinition(id="bug_hunter_bronze", name="Hunter", description="5 Quests", rarity="common", xp_bonus=100),
        BadgeDefinition(id="perfectionist", name="Perfect", description="100% Score", rarity="epic", xp_bonus=500)
    ]
    for b in badges:
        db_session.add(b)
    
    # Create User
    user = User(id="player1", name="Player One")
    db_session.add(user)
    await db_session.commit()

async def test_progressive_unlocks(db_session, achievement_setup):
    """Verify badges unlock sequentially as stats increase."""
    
    # Mock Redis to avoid connection errors during test
    with patch("arcade_app.gamification.Redis.from_url", return_value=AsyncMock()):
        
        # 1. Complete 1st Quest -> Should unlock 'hello_world'
        await process_quest_completion("player1", "world-python", 80)
        
        badges = (await db_session.exec(select(UserBadge).where(UserBadge.user_id == "player1"))).all()
        assert len(badges) == 1
        assert badges[0].badge_id == "hello_world"

        # 2. Complete 3 more quests (Total 4) -> No new badge (Need 5)
        for _ in range(3):
            await process_quest_completion("player1", "world-python", 80)
        
        badges = (await db_session.exec(select(UserBadge).where(UserBadge.user_id == "player1"))).all()
        assert len(badges) == 1 # Still just 1

        # 3. Complete 5th Quest -> Unlock 'bug_hunter_bronze'
        await process_quest_completion("player1", "world-python", 80)
        
        badges = (await db_session.exec(select(UserBadge).where(UserBadge.user_id == "player1"))).all()
        assert len(badges) == 2
        assert any(b.badge_id == "bug_hunter_bronze" for b in badges)

async def test_perfect_score_logic(db_session, achievement_setup):
    """Verify specific conditions (score >= 100) trigger specific badges."""
    
    with patch("arcade_app.gamification.Redis.from_url", return_value=AsyncMock()):
        # 1. Submit Average Code (Score 90)
        await process_quest_completion("player1", "world-python", 90)
        
        # Check Metrics
        metric = await db_session.get(UserMetric, "player1")
        assert metric.perfect_scores == 0
        
        # 2. Submit Perfect Code (Score 100)
        await process_quest_completion("player1", "world-python", 100)
        
        # Verify Metric & Badge
        await db_session.refresh(metric)
        assert metric.perfect_scores == 1
        
        badges = (await db_session.exec(select(UserBadge).where(UserBadge.user_id == "player1"))).all()
        assert any(b.badge_id == "perfectionist" for b in badges)

import pytest
import pytest_asyncio
from sqlmodel import select
from arcade_app.models import User, Profile, SkillNode, UserSkill
from arcade_app.skill_helper import get_skill_tree, unlock_skill

# Mark all async tests
pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture
async def skill_setup(db_session):
    """Seeds the DB with a mini skill tree and a user."""
    # 1. Create Tree
    # Root -> Child
    root = SkillNode(id="root", name="Root", description="Root Skill", cost=1, tier=1, category="test", feature_key="root_feat")
    child = SkillNode(id="child", name="Child", description="Child Skill", cost=2, tier=2, category="test", feature_key="child_feat", parent_id="root")
    
    db_session.add(root)
    db_session.add(child)
    
    # 2. Create User (3 SP)
    user = User(id="player1", name="Player One")
    profile = Profile(user_id="player1", total_xp=0, global_level=1, skill_points=3)
    
    db_session.add(user)
    db_session.add(profile)
    await db_session.commit()

async def test_get_tree_status(db_session, skill_setup):
    """Verify initial state: Root unlockable, Child locked."""
    data = await get_skill_tree("player1")
    
    assert data["skill_points"] == 3
    nodes = data["nodes"]
    
    root = next(n for n in nodes if n["id"] == "root")
    child = next(n for n in nodes if n["id"] == "child")
    
    # Root: Can unlock (Has points, no parent)
    assert root["is_unlocked"] is False
    assert root["can_unlock"] is True
    
    # Child: Cannot unlock (Parent not owned)
    assert child["is_unlocked"] is False
    assert child["can_unlock"] is False

async def test_unlock_flow(db_session, skill_setup):
    """Verify purchasing a skill works and updates state."""
    # 1. Unlock Root
    res = await unlock_skill("player1", "root")
    assert res["status"] == "ok"
    assert res["remaining_sp"] == 2 # 3 - 1
    
    # 2. Verify Persistence
    # Use expire_all to force fresh read
    db_session.expire_all()
    
    # Check Profile
    profile = await db_session.execute(select(Profile).where(Profile.user_id == "player1"))
    assert profile.scalars().first().skill_points == 2
    
    # Check Unlock Record
    unlock = await db_session.execute(select(UserSkill).where(UserSkill.user_id == "player1", UserSkill.skill_id == "root"))
    assert unlock.scalars().first() is not None

    # 3. Verify Child is now unlockable
    data = await get_skill_tree("player1")
    child = next(n for n in data["nodes"] if n["id"] == "child")
    assert child["can_unlock"] is True

async def test_unlock_insufficient_funds(db_session, skill_setup):
    """Verify you can't buy what you can't afford."""
    # Set SP to 0
    profile_res = await db_session.execute(select(Profile).where(Profile.user_id == "player1"))
    profile = profile_res.scalars().first()
    profile.skill_points = 0
    db_session.add(profile)
    await db_session.commit()
    
    res = await unlock_skill("player1", "root")
    assert "error" in res
    assert "Insufficient" in res["error"]

async def test_unlock_dependency_check(db_session, skill_setup):
    """Verify you can't skip the tree hierarchy."""
    # Try to unlock Child without Root
    res = await unlock_skill("player1", "child")
    assert "error" in res
    assert "Dependency not met" in res["error"]

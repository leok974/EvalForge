import pytest
from httpx import AsyncClient
from sqlmodel import select
from arcade_app.models import User, Profile, QuestProgress, BossRun, QuestState, BossDefinition
from arcade_app.practice.constants import SENIOR_BOSS_IDS, SENIOR_TRACK_IDS_BY_WORLD
from datetime import datetime
from unittest.mock import patch, MagicMock

# Mark as async test
import pytest_asyncio
pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture
async def test_user(db_session):
    user_id = "test_senior_user"
    user = User(id=user_id, name="Senior Tester")
    db_session.add(user)
    try:
        await db_session.commit()
    except Exception: 
        await db_session.rollback()
        user = (await db_session.exec(select(User).where(User.id == user_id))).first()
    return user

@pytest.fixture
def mock_auth(test_user, db_session):
    from arcade_app.database import get_session
    from arcade_app.agent import app
    
    # Mock return value
    auth_user = {"id": test_user.id, "name": test_user.name}
    
    # 2. Mock DB Session (Share test transaction)
    # This IS used via Depends, so override works.
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session
    
    # 1. Patch get_current_user in the router modules
    # Since they call it directly.
    patcher1 = patch("arcade_app.routers.routes_profile.get_current_user", new=MagicMock(return_value=auth_user))
    patcher2 = patch("arcade_app.routers.routes_boss_runs.get_current_user", new=MagicMock(return_value=auth_user))
    
    # Async mock needed? get_current_user is async.
    # MagicMock is synchronous. Accessing it returns Mock.
    # We need an AsyncMock.
    from unittest.mock import AsyncMock
    async_mock = AsyncMock(return_value=auth_user)
    
    patcher1 = patch("arcade_app.routers.routes_profile.get_current_user", new=async_mock)
    patcher2 = patch("arcade_app.routers.routes_boss_runs.get_current_user", new=async_mock)
    
    # 3. Patch WORLDS data
    mock_worlds = {
        "world-python": {"id": "world-python", "title": "Python World"},
        "world-ml": {"id": "world-ml", "title": "ML World"}
    }
    patch_worlds = patch.dict("arcade_app.agent.WORLDS", mock_worlds, clear=True)
    
    patcher1.start()
    patcher2.start()
    patch_worlds.start()
    
    yield
    
    patch_worlds.stop()
    patcher1.stop()
    patcher2.stop()
    app.dependency_overrides = {}

async def test_senior_progress_api(client: AsyncClient, db_session, test_user: User, mock_auth):
    """
    Verify /api/profile/senior_progress returns correct aggregation.
    """
    # 1. Setup Data
    # Ensure profile exists (created by fixture usually, but verify)
    profile = (await db_session.exec(select(Profile).where(Profile.user_id == test_user.id))).first()
    if not profile:
        profile = Profile(user_id=test_user.id, username="test_senior")
        db_session.add(profile)
        await db_session.commit()

    # Create a senior boss run (Win)
    senior_boss_id = "boss-foundry-systems-architect"
    
    boss_def = BossDefinition(
        id=senior_boss_id,
        name="Mock Senior Boss",
        track_id="foundry-senior-systems",
        world_id="world-python",
        difficulty="legendary"
    )
    db_session.add(boss_def) 
    
    # Add a run
    run = BossRun(
        user_id=test_user.id,
        boss_id=senior_boss_id,
        result="win",
        score=100,
        hp_remaining=0,
        completed_at=datetime.utcnow()
    )
    db_session.add(run)
    await db_session.commit()

    # 2. Call API
    resp = await client.get("/api/profile/senior_progress")
    assert resp.status_code == 200, f"Failed: {resp.text}"
    
    data = resp.json()
    
    # 3. Assertions
    assert data["senior_bosses_cleared"] >= 1
    assert data["legendary_trials_completed"] >= 1
    
    # Python World Verification (slug="world-python")
    python_world = next((w for w in data["worlds"] if w["world_slug"] == "world-python"), None)
    assert python_world is not None
    assert python_world["senior_boss_cleared"] is True
    assert python_world["senior_boss_id"] == senior_boss_id

async def test_senior_boss_runs_api(client: AsyncClient, db_session, test_user: User, mock_auth):
    """
    Verify /api/boss_runs/senior returns the history.
    """
    # 1. Setup Data
    senior_boss_id = "boss-synapse-mlops-sentinel" # ML Senior
    
    boss_def = BossDefinition(
        id=senior_boss_id,
        name="ML Sentinel",
        track_id="synapse-senior-mlops",
        world_id="world-ml",
        difficulty="legendary"
    )
    db_session.add(boss_def)
    
    run = BossRun(
        user_id=test_user.id,
        boss_id=senior_boss_id,
        result="win",
        score=8,
        hp_remaining=90, # 90% integrity
        completed_at=datetime.utcnow()
    )
    db_session.add(run)
    await db_session.commit()
    
    # 2. Call API
    resp = await client.get("/api/boss_runs/senior")
    assert resp.status_code == 200
    
    data = resp.json()
    items = data["items"]
    
    assert len(items) >= 1
    item = items[0]
    assert item["boss_id"] == senior_boss_id
    assert item["passed"] is True
    assert item["score"] == 8
    # Integrity check: backend casts to float. 90 -> 90.0
    assert item["integrity"] == 90.0

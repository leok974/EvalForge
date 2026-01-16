import pytest
from httpx import AsyncClient
from sqlmodel import select
from arcade_app.models import QuestProgress, QuestDefinition, Profile, User, QuestState
from arcade_app.practice.constants import STARTER_WORLD_SLUG, STARTER_QUEST_ID
from arcade_app.agent import app
from arcade_app.auth_helper import get_current_user

# Mock User
TEST_USER_ID = "test_profile_user"
TEST_USER = {
    "id": TEST_USER_ID,
    "user_id": TEST_USER_ID,
    "email": "test@example.com",
    "login": "testuser",
    "name": "Test User"
}

# Override Dependency
from arcade_app.database import get_session

# Mock User Global
async def mock_get_current_user():
    return TEST_USER

app.dependency_overrides[get_current_user] = mock_get_current_user

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200, f"Health check failed: {response.text}"

@pytest.mark.asyncio
async def test_profile_me_unlocks_starter_quest(client: AsyncClient, db_session):
    """
    Verifies that calling /api/profile/me:
    1. Creates a profile if missing.
    2. Automatically unlocks the starter quest via ensure_starter_unlocked.
    """
    # OVERRIDE SESSION: Share transaction
    async def override_get_session():
        yield db_session
    app.dependency_overrides[get_session] = override_get_session
    
    # 0. Seed Quest Definition (FK Constraint)
    # We must ensure the quest definition exists, otherwise FK fails.
    q_def = QuestDefinition(
        slug=STARTER_QUEST_ID,
        title="Starter Quest",
        short_description="Start here",
        world_id=STARTER_WORLD_SLUG,
        track_id="track-01"
    )
    db_session.add(q_def)
    await db_session.commit()
    
    # 1. Call /api/profile/me
    response = await client.get("/api/profile/me")
    if response.status_code != 200:
        pytest.fail(f"API Error: {response.status_code} {response.text}")
    data = response.json()
    assert data["user_id"] == TEST_USER_ID
    profile_id = data["id"]
    
    # 2. Verify Quest Progress Exists
    stmt = select(QuestProgress).where(
        QuestProgress.user_id == TEST_USER_ID, # QuestProgress uses user_id now
        QuestProgress.quest_id == q_def.id
    )
    result = await db_session.exec(stmt)
    qp = result.first()
    
    if qp is None:
        q_debug = await db_session.exec(select(QuestDefinition))
        qs = [ (x.id, x.slug) for x in q_debug.all() ]
        pytest.fail(f"QuestProgress not found. Available Quests: {qs}. UserID: {TEST_USER_ID}")
        
    assert qp.state == QuestState.AVAILABLE
    
    # 3. Call again (Idempotency)
    response_2 = await client.get("/api/profile/me")
    assert response_2.status_code == 200
    
    result_2 = await db_session.exec(stmt)
    qp_list = result_2.all()
    assert len(qp_list) == 1  # Should not duplicate

@pytest.mark.asyncio
async def test_profile_me_backfills_unlock_for_existing_profile(client: AsyncClient, db_session):
    """
    Test scenario where profile exists but quest is NOT unlocked.
    Calling /me should fix it.
    """
    # OVERRIDE SESSION
    async def override_get_session():
        yield db_session
    app.dependency_overrides[get_session] = override_get_session

    # 0. Seed Quest & User & Profile
    q_def = QuestDefinition(
        slug=STARTER_QUEST_ID,
        title="Starter Quest",
        short_description="Start here",
        world_id=STARTER_WORLD_SLUG,
        track_id="track-01"
    )
    db_session.add(q_def)
    
    user = User(id=TEST_USER_ID + "_existing", name="Existing User")
    db_session.add(user)
    
    profile = Profile(user_id=user.id)
    db_session.add(profile)
    await db_session.commit()
    await db_session.refresh(profile)

    # Mock user for THIS test
    async def mock_existing_user():
        return {"id": user.id}
    app.dependency_overrides[get_current_user] = mock_existing_user

    # Verify no progress yet
    stmt = select(QuestProgress).where(
        QuestProgress.user_id == user.id,
        QuestProgress.quest_id == q_def.id
    )
    assert (await db_session.exec(stmt)).first() is None
    
    # 1. Call /api/profile/me
    response = await client.get("/api/profile/me")
    assert response.status_code == 200
    
    # 2. Verify Now Unlocked
    qp = (await db_session.exec(stmt)).first()
    assert qp is not None
    assert qp.state == QuestState.AVAILABLE


import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from arcade_app.main import app
from arcade_app.models import QuestDefinition, Profile
from arcade_app.auth_helper import get_current_user
from sqlmodel import Session, select
from arcade_app.services.quest_visibility import get_active_quest_config

# --- Fixtures ---

@pytest.fixture
def mock_user():
    return {"id": "test_visibility_user", "name": "Visibility Tester", "auth_mode": "mock"}

@pytest_asyncio.fixture
async def authenticated_client(mock_user):
    # Override Auth
    app.dependency_overrides[get_current_user] = lambda: mock_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    # Cleanup
    app.dependency_overrides = {}

# --- Tests ---

@pytest.mark.asyncio
async def test_quests_default_visibility_active_only(authenticated_client, db_session):
    # 1. Setup: Seed a fake requester profile
    user_id = "test_visibility_user"
    if not await db_session.get(Profile, user_id):
        db_session.add(Profile(user_id=user_id))
        await db_session.commit()

    # 2. Seed a fake quest that is definitely NOT in active config
    fake_inactive_slug = "quest-fake-inactive" 
    fake_quest = QuestDefinition(
        slug=fake_inactive_slug,
        title="Fake Inactive Quest",
        world_id="world-test",
        track_id="track-test",
        order_index=999,
        short_description="Fake Short Description",
        detailed_description="Fake Detailed Description"
    )
    db_session.add(fake_quest)
    await db_session.commit()

    # 3. Query default endpoint
    response = await authenticated_client.get("/api/quests")
    assert response.status_code == 200, f"Response: {response.text}"
    quests = response.json()
    slugs = [q["slug"] for q in quests]
    
    # 4. Assertions
    assert fake_inactive_slug not in slugs
    
    # Verify Metadata Injection
    # Just check the first one if it exists
    if quests:
        assert "is_active" in quests[0]
        assert "questpack" in quests[0]

@pytest.mark.asyncio
async def test_quests_include_inactive_flag(authenticated_client, db_session):
    # 1. Setup
    fake_slug = "quest-fake-admin-visible"
    fake_quest = QuestDefinition(
        slug=fake_slug,
        title="Fake Admin Quest",
        world_id="world-test",
        track_id="track-test",
        order_index=999,
        short_description="Fake Short Description",
        detailed_description="Fake Detailed Description"
    )
    db_session.add(fake_quest)
    await db_session.commit()
    
    # 2. Query with flag
    response = await authenticated_client.get("/api/quests?include_inactive=true")
    assert response.status_code == 200
    quests = response.json()
    slugs = [q["slug"] for q in quests]
    
    # 3. Assert
    assert fake_slug in slugs

@pytest.mark.asyncio
async def test_canary_quest_hidden_by_default(authenticated_client, db_session):
    # Verify the specific requirement: quest-py-hidden must be hidden
    canary_slug = "quest-py-hidden"
    
    # Ensure it exists in DB (simulate seeding)
    res = await db_session.exec(select(QuestDefinition).where(QuestDefinition.slug == canary_slug))
    if not res.first():
        db_session.add(QuestDefinition(
            slug=canary_slug,
            title="Canary Hidden",
            world_id="world-python",
            track_id="track-python",
            order_index=999,
            short_description="Canary Short",
            detailed_description="Canary Detailed"
        ))
        await db_session.commit()
        
    # Default fetch
    response = await authenticated_client.get("/api/quests")
    slugs = [q["slug"] for q in response.json()]
    
    assert canary_slug not in slugs, "Canary quest should be hidden by default"
    
    # Admin fetch
    response_admin = await authenticated_client.get("/api/quests?include_inactive=true")
    slugs_admin = [q["slug"] for q in response_admin.json()]
    
    assert canary_slug in slugs_admin, "Canary quest should be visible with admin flag"

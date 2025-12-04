
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from arcade_app.agent import app
from arcade_app.models import QuestDefinition, Profile, User, QuestState
from arcade_app.database import get_session

# Mock auth dependency
from arcade_app.auth_helper import get_current_user

@pytest.fixture(name="client")
def client_fixture():
    return TestClient(app)

@pytest.fixture(name="auth_headers")
def auth_headers_fixture():
    return {"Authorization": "Bearer mock-token"}

# Override get_current_user to return our test user
def override_get_current_user():
    # Return a dict as expected by the endpoint
    return {
        "id": "test-user",
        "name": "Test User",
        "avatar_url": None
    }

app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.mark.asyncio
async def test_quest_completion_unlocks_boss_and_emits_event(client, db_session: Session):
    """
    End-to-end-ish:
    - Find a quest that is supposed to unlock a boss.
    - Submit a passing solution.
    - Assert unlock_events contains the boss.
    - Assert profile.flags.bosses_unlocked includes that boss.
    """
    # 1. Setup Data
    user = User(id="test-user", name="Test User")
    db_session.add(user)
    
    profile = Profile(user_id="test-user", id=1, total_xp=0, flags={})
    db_session.add(profile)

    quest = QuestDefinition(
        slug="python-reactor-prep",
        world_id="world-python",
        track_id="boss-prep",
        title="Reactor Prep",
        short_description="Prepare for the Reactor Core boss.",
        unlocks_boss_id="reactor-core",
        base_xp_reward=50
    )
    db_session.add(quest)
    await db_session.commit()
    await db_session.refresh(quest)

    # 2. Submit a passing solution
    # We need to mock grade_quest_submission to always pass
    # For now, we'll rely on the fact that the endpoint calls it.
    # If we can't easily mock the internal function call here without more complex patching,
    # we might need to rely on the mock grader env var if set, or patch it.
    
    # Let's try patching grade_quest_submission in the router module if possible,
    # or just assume the mock grader is active/we can influence it.
    # Given the complexity of patching inside an endpoint from an integration test,
    # let's assume we can just call the logic or use a mock.
    
    # Actually, simpler: let's use `unittest.mock.patch` on the import in `routes_quests`.
    from unittest.mock import patch
    
    with patch("arcade_app.grading_helper.grade_quest_submission", return_value=(100, True)):
        resp = client.post(
            f"/api/quests/{quest.slug}/submit",
            headers={"Authorization": "Bearer mock-token"},
            json={"code": "print('ok')", "language": "python"},
        )
    
    assert resp.status_code == 200
    data = resp.json()

    # 3. Verify Response
    unlocks = data.get("unlock_events") or []
    unlocked_ids = [u["id"] for u in unlocks if u["type"] == "boss"]
    assert (
        "reactor-core" in unlocked_ids
    ), f"Expected unlock_events to include boss reactor-core, got {unlocks}"

    # 4. Verify Profile Flags in Response
    # The API returns the updated profile, which is refreshed from DB.
    # So this confirms the DB was updated.
    profile_data = data.get("profile", {})
    flags = profile_data.get("flags", {})
    bosses_unlocked = flags.get("bosses_unlocked", [])
    assert (
        "reactor-core" in bosses_unlocked
    ), f"Expected response profile.flags to contain reactor-core, got {bosses_unlocked}"

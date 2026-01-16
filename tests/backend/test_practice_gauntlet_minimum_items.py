import pytest
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from arcade_app.models import User, Profile, QuestDefinition, QuestProgress, QuestState
from arcade_app.practice.starter import ensure_starter_unlocked
from arcade_app.practice.constants import STARTER_WORLD_SLUG, STARTER_QUEST_ID
from arcade_app.agent import app
from arcade_app.auth_helper import get_current_user

@pytest.mark.asyncio
async def test_practice_gauntlet_returns_items_for_new_player(db_session: AsyncSession, client):
    """
    For a brand-new profile with no progress, ensure_starter_unlocked should give them
    a starter quest, and the Practice Gauntlet API should surface at least one item.
    """
    session = db_session
    user_id = "test-user-gauntlet-1"

    # --- Arrange: Create User, Profile, QuestDefinition ---
    user = User(id=user_id, name="Gauntlet Test 1")
    session.add(user)
    
    profile = Profile(
        user_id=user.id,
        total_xp=0,
        global_level=1,
        world_progress={}
    )
    session.add(profile)
    
    # Needs quest def matching STARTER_QUEST_ID (slug)
    # Using 998 to avoid conflict with starter test (999) if they run in parallel or don't clean up
    q_def = QuestDefinition(
        id=998, 
        slug=STARTER_QUEST_ID,
        title="Starter Quest",
        world_id=STARTER_WORLD_SLUG,
        track_id="python-core",
        order_index=1,
        short_description="Start here",
        detailed_description="...",
        rubric_id="rubric1",
        base_xp_reward=100
    )
    session.add(q_def)
    
    await session.commit()
    await session.refresh(profile)

    # Sanity: no progress yet
    count_before = await session.scalar(
        select(func.count(QuestProgress.id)).where(
            QuestProgress.user_id == profile.user_id
        )
    )
    assert count_before == 0

    # --- Act: ensure starter quest is unlocked ---
    await ensure_starter_unlocked(session, profile)

    # Sanity: now there should be at least one QuestProgress row
    count_after = await session.scalar(
        select(func.count(QuestProgress.id)).where(
            QuestProgress.user_id == profile.user_id
        )
    )
    assert count_after >= 1

    # --- Mock Auth ---
    async def mock_user_dep():
        return {
            "id": user_id,
            "name": "Gauntlet Test 1",
            "auth_mode": "mock",
            "dev_unlock_all_features": False
        }
    
    app.dependency_overrides[get_current_user] = mock_user_dep

    try:
        # --- Assert: Practice Gauntlet API returns at least one item ---
        resp = await client.get("/api/practice_rounds/today")
        assert resp.status_code == 200, resp.text

        data = resp.json()
        assert "items" in data
        assert isinstance(data["items"], list)
        
        # KEY ASSERTION: At least one item
        assert len(data["items"]) >= 1
        
        # Verify total_count
        assert "total_count" in data
        assert data["total_count"] >= 1

    finally:
        del app.dependency_overrides[get_current_user]

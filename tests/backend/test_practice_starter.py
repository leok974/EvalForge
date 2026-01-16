import pytest
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from arcade_app.practice.starter import ensure_starter_unlocked
from arcade_app.practice.constants import STARTER_WORLD_SLUG, STARTER_QUEST_ID
from arcade_app.models import QuestProgress, Profile, User, QuestState

@pytest.mark.asyncio
async def test_ensure_starter_unlocked_creates_progress_for_new_profile(db_session: AsyncSession):
    """
    When a brand-new profile has no quest progress, ensure_starter_unlocked
    should create exactly one QuestProgress row pointing at the starter quest.
    """
    session = db_session

    # Create user first (FK constraint)
    user = User(id="test-user-starter-1", name="Starter Test 1")
    session.add(user)
    
    # Create profile
    profile = Profile(
        user_id=user.id,
        total_xp=0,
        global_level=1,
        world_progress={}
    )
    session.add(profile)
    
    # Seed Starter Quest Definition (Required for FK)
    from arcade_app.models import QuestDefinition
    q_def = QuestDefinition(
        id=999, # Arbitrary INT
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

    # Act
    await ensure_starter_unlocked(session, profile)

    # Assert: one progress row exists for starter quest
    rows = (
        await session.execute(
            select(QuestProgress).where(
                QuestProgress.user_id == profile.user_id
            )
        )
    ).scalars().all()

    assert len(rows) == 1
    starter = rows[0]
    # assert starter.world_slug == STARTER_WORLD_SLUG # Model doesn't have it
    assert starter.quest_id == 999 
    assert starter.state == "AVAILABLE" or starter.state == QuestState.AVAILABLE


@pytest.mark.asyncio
async def test_ensure_starter_unlocked_is_idempotent(db_session: AsyncSession):
    """
    If the profile already has quest progress, ensure_starter_unlocked should
    NOT create a duplicate starter quest row.
    """
    session = db_session

    # Create user first
    user = User(id="test-user-starter-2", name="Starter Test 2")
    session.add(user)

    profile = Profile(
        user_id=user.id,
        total_xp=0,
        global_level=1,
        world_progress={}
    )
    session.add(profile)
    
    # Needs quest def too
    from arcade_app.models import QuestDefinition
    q_def = QuestDefinition(
        id=888, 
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

    # Seed an existing progress row (could be starter or something else)
    existing = QuestProgress(
        user_id=profile.user_id,
        # world_slug=STARTER_WORLD_SLUG, 
        quest_id=888,
        state=QuestState.AVAILABLE,
        attempts=0
    )
    session.add(existing)
    await session.commit()

    # Act
    await ensure_starter_unlocked(session, profile)

    # Assert: still exactly one row for this profile
    rows = (
        await session.execute(
            select(QuestProgress).where(
                QuestProgress.user_id == profile.user_id
            )
        )
    ).scalars().all()

    assert len(rows) == 1
    assert rows[0].id == existing.id

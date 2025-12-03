import pytest
import pytest_asyncio
from arcade_app.models import User, Profile, BossDefinition, BossRun, BossCodexProgress
from arcade_app.boss_codex_helper import on_boss_failure, on_boss_success, get_or_create_progress

@pytest_asyncio.fixture
async def profile(db_session):
    user = User(id="test_user", name="Test User")
    db_session.add(user)
    await db_session.commit()
    
    profile = Profile(user_id=user.id)
    db_session.add(profile)
    await db_session.commit()
    return profile

@pytest_asyncio.fixture
async def reactor_boss_def(db_session):
    boss = BossDefinition(
        id="boss-reactor-core",
        name="The Reactor Core",
        world_id="world-python",
        hint_codex_id="boss-reactor-core-strategy"
    )
    db_session.add(boss)
    await db_session.commit()
    return boss

@pytest_asyncio.fixture
async def reactor_encounter(db_session, profile, reactor_boss_def):
    encounter = BossRun(
        user_id=profile.user_id,
        boss_id=reactor_boss_def.id
    )
    db_session.add(encounter)
    await db_session.commit()
    return encounter

@pytest.mark.asyncio
async def test_first_failure_unlocks_tier1(db_session, profile, reactor_boss_def, reactor_encounter):
    progress = await get_or_create_progress(db_session, profile.id, reactor_boss_def.id)
    assert progress.tier_unlocked == 0
    assert progress.deaths == 0

    await on_boss_failure(db_session, profile, reactor_boss_def)
    # Re-fetch
    await db_session.refresh(progress)

    assert progress.deaths == 1
    assert progress.tier_unlocked >= 1

@pytest.mark.asyncio
async def test_multiple_failures_unlock_tier2(db_session, profile, reactor_boss_def, reactor_encounter):
    progress = await get_or_create_progress(db_session, profile.id, reactor_boss_def.id)
    
    # Simulate 3 deaths
    for _ in range(3):
        await on_boss_failure(db_session, profile, reactor_boss_def)
    
    await db_session.refresh(progress)

    assert progress.deaths >= 3
    assert progress.tier_unlocked >= 2

@pytest.mark.asyncio
async def test_first_kill_unlocks_tier3(db_session, profile, reactor_boss_def, reactor_encounter):
    progress = await get_or_create_progress(db_session, profile.id, reactor_boss_def.id)
    
    await on_boss_success(db_session, profile, reactor_boss_def)
    await db_session.refresh(progress)

    assert progress.wins == 1
    assert progress.first_kill_at is not None
    assert progress.tier_unlocked == 3

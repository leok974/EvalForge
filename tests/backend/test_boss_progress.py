import pytest
from sqlmodel import select
from arcade_app.models import BossProgress, User, BossDefinition
from arcade_app.bosses.boss_progress_helper import update_boss_progress

@pytest.mark.asyncio
async def test_boss_progress_flow(async_session):
    # 1. Setup Data
    user = User(id="test_user_progress", name="Test User")
    boss = BossDefinition(id="boss-test", name="Test Boss")
    async_session.add(user)
    async_session.add(boss)
    await async_session.commit()

    # 2. First Failure
    res1 = await update_boss_progress(
        async_session, 
        user_id="test_user_progress", 
        boss_id="boss-test", 
        outcome="fail"
    )
    assert res1["fail_streak"] == 1
    assert res1["hint_unlocked"] is False

    # 3. Second Failure (Should Unlock Hint)
    # Note: Helper uses HINT_UNLOCK_THRESHOLD = 2
    # And requires BOSS_HINT_MAP to have the boss_id
    from arcade_app.bosses.boss_progress_helper import BOSS_HINT_MAP
    BOSS_HINT_MAP["boss-test"] = "hint-test-codex"

    res2 = await update_boss_progress(
        async_session, 
        user_id="test_user_progress", 
        boss_id="boss-test", 
        outcome="fail"
    )
    assert res2["fail_streak"] == 2
    assert res2["hint_unlocked"] is True
    assert res2["hint_codex_id"] == "hint-test-codex"

    # 4. Verify DB State
    stmt = select(BossProgress).where(BossProgress.user_id == "test_user_progress")
    progress = (await async_session.execute(stmt)).scalar_one()
    assert progress.fail_streak == 2
    assert progress.highest_hint_level == 1

    # 5. Success (Should Reset Streak)
    res3 = await update_boss_progress(
        async_session, 
        user_id="test_user_progress", 
        boss_id="boss-test", 
        outcome="win"
    )
    assert res3["fail_streak"] == 0
    
    # Verify DB State after win
    await async_session.refresh(progress)
    assert progress.fail_streak == 0
    assert progress.last_result == "win"

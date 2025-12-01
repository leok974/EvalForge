"""
Tests for boss progress tracking and adaptive hint system.
"""
import pytest
from datetime import datetime, UTC
from sqlmodel import select
from arcade_app.models import BossProgress
from arcade_app.bosses.boss_progress_helper import update_boss_progress, HINT_UNLOCK_THRESHOLD


@pytest.mark.asyncio
async def test_first_failure_no_hint(db_session):
    """First failure should increment streak but not unlock hint."""
    result = await update_boss_progress(
        db_session,
        user_id="test_user",
        boss_id="boss-reactor-core",
        outcome="fail"
    )
    
    assert result["fail_streak"] == 1
    assert result["hint_codex_id"] is None


@pytest.mark.asyncio
async def test_second_failure_unlocks_hint(db_session):
    """Second consecutive failure should unlock strategy guide."""
    # First failure
    await update_boss_progress(
        db_session,
        user_id="test_user",
        boss_id="boss-reactor-core",
        outcome="fail"
    )
    
    # Second failure
    result = await update_boss_progress(
        db_session,
        user_id="test_user",
        boss_id="boss-reactor-core",
        outcome="fail"
    )
    
    assert result["fail_streak"] == 2
    assert result["hint_codex_id"] == "boss-reactor-core"


@pytest.mark.asyncio
async def test_win_resets_streak(db_session):
    """Winning should reset fail streak to zero."""
    # Fail twice
    await update_boss_progress(db_session, "test_user", "boss-reactor-core", "fail")
    await update_boss_progress(db_session, "test_user", "boss-reactor-core", "fail")
    
    # Win resets
    result = await update_boss_progress(
        db_session,
        user_id="test_user",
        boss_id="boss-reactor-core",
        outcome="win"
    )
    
    assert result["fail_streak"] == 0
    assert result["hint_codex_id"] is None


@pytest.mark.asyncio
async def test_fail_after_win_starts_new_streak(db_session):
    """After winning, failures should start a new streak from 1."""
    # Win first
    await update_boss_progress(db_session, "test_user", "boss-reactor-core", "win")
    
    # Fail again
    result = await update_boss_progress(
        db_session,
        user_id="test_user",
        boss_id="boss-reactor-core",
        outcome="fail"
    )
    
    assert result["fail_streak"] == 1
    assert result["hint_codex_id"] is None


@pytest.mark.asyncio
async def test_multiple_users_independent_streaks(db_session):
    """Different users should have independent fail streaks."""
    # User 1 fails twice
    result1 = await update_boss_progress(db_session, "user1", "boss-reactor-core", "fail")
    result1 = await update_boss_progress(db_session, "user1", "boss-reactor-core", "fail")
    
    # User 2 fails once
    result2 = await update_boss_progress(db_session, "user2", "boss-reactor-core", "fail")
    
    assert result1["fail_streak"] == 2
    assert result1["hint_codex_id"] == "boss-reactor-core"
    
    assert result2["fail_streak"] == 1
    assert result2["hint_codex_id"] is None


@pytest.mark.asyncio
async def test_progress_persists_in_db(db_session):
    """Progress should be persisted to database."""
    await update_boss_progress(
        db_session,
        user_id="test_user",
        boss_id="boss-reactor-core",
        outcome="fail"
    )
    
    # Query directly from DB
    stmt = select(BossProgress).where(
        BossProgress.user_id == "test_user",
        BossProgress.boss_id == "boss-reactor-core"
    )
    result = await db_session.exec(stmt)
    progress = result.first()
    
    assert progress is not None
    assert progress.fail_streak == 1
    assert progress.last_outcome == "fail"


@pytest.mark.asyncio
async def test_unknown_boss_no_hint(db_session):
    """Bosses not in BOSS_HINT_MAP should not unlock hints."""
    # Fail twice on unknown boss
    result = await update_boss_progress(db_session, "test_user", "unknown-boss", "fail")
    result = await update_boss_progress(db_session, "test_user", "unknown-boss", "fail")
    
    assert result["fail_streak"] == 2
    assert result["hint_codex_id"] is None  # No hint for unknown bosses

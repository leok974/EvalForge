"""Helper for tracking boss progress and unlocking adaptive hints."""
from datetime import datetime, UTC
from sqlmodel import select
from arcade_app.models import BossProgress

# Boss-to-Codex mapping for strategy guides
BOSS_HINT_MAP = {
    "boss-reactor-core": "boss-reactor-core",
    "reactor_core": "boss-reactor-core",
}

# Unlock threshold: Show hint after N consecutive failures
HINT_UNLOCK_THRESHOLD = 2


async def update_boss_progress(
    session,
    user_id: str,
    boss_id: str,
    outcome: str  # 'win' or 'fail'
) -> dict:
    """
    Update long-term boss progress tracking.
    
    Increments fail streak on losses, resets on wins.
    Unlocks strategy guide hints after HINT_UNLOCK_THRESHOLD consecutive failures.
    
    Args:
        session: Database session
        user_id: User identifier
        boss_id: Boss identifier (e.g. "boss-reactor-core")
        outcome: "win" or "fail"
        
    Returns:
        Dict with fail_streak, hint_codex_id, and hint_unlocked flag
    """
    # Fetch or create progress record
    stmt = select(BossProgress).where(
        BossProgress.user_id == user_id,
        BossProgress.boss_id == boss_id
    )
    result = await session.execute(stmt)
    progress = result.scalar_one_or_none()
    
    if not progress:
        progress = BossProgress(
            user_id=user_id,
            boss_id=boss_id,
            fail_streak=0,
            highest_hint_level=0,
            last_attempt_at=datetime.now(UTC),
            last_result=None,
        )
        session.add(progress)
    
    # Update streaks
    hint_unlocked = False
    hint_codex_id = None
    
    if outcome == "win":
        progress.fail_streak = 0
        progress.last_result = "win"
    else:  # fail
        progress.fail_streak += 1
        progress.last_result = "fail"
        
        # Check if we should unlock a hint
        if progress.fail_streak >= HINT_UNLOCK_THRESHOLD:
            # Only unlock if not already at this level
            if progress.highest_hint_level < 1:
                progress.highest_hint_level = 1
                hint_unlocked = True
            
            # Return hint ID if boss is in the map
            hint_codex_id = BOSS_HINT_MAP.get(boss_id)
    
    progress.last_attempt_at = datetime.now(UTC)
    
    await session.commit()
    await session.refresh(progress)
    
    return {
        "fail_streak": progress.fail_streak,
        "hint_codex_id": hint_codex_id,
        "hint_unlocked": hint_unlocked,
        "highest_hint_level": progress.highest_hint_level,
    }

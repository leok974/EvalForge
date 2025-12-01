from __future__ import annotations

from sqlmodel import select
from arcade_app.bosses.types import BossOutcome
from arcade_app.models import Profile, BossRun
from arcade_app.database import get_session


async def apply_boss_outcome(user_id: str, outcome: BossOutcome) -> None:
    """
    Apply XP and integrity changes to the user's Profile.
    """
    async for session in get_session():
        stmt = select(Profile).where(Profile.user_id == user_id)
        result = await session.execute(stmt)
        profile = result.scalars().first()

        if not profile:
            # Create a new profile if needed (should exist though)
            profile = Profile(user_id=user_id, total_xp=0, integrity=100)
            session.add(profile)

        # XP
        if outcome.xp_awarded:
            profile.total_xp += outcome.xp_awarded

        # Integrity (HP)
        if outcome.integrity_delta:
            profile.integrity += outcome.integrity_delta
            # clamp
            if profile.integrity > profile.max_integrity:
                profile.integrity = profile.max_integrity
            if profile.integrity < 0:
                profile.integrity = 0

        session.add(profile)
        await session.commit()
        break  # just one session iteration


async def record_boss_run(
    session,
    user_id: str,
    boss_id: str,
    difficulty: str,
    score: int,
    passed: bool,
    integrity_delta: int,
    xp_awarded: int,
) -> None:
    """
    Persist a completed boss run to the BossRun table for history tracking.
    
    Args:
        session: Async database session
        user_id: ID of the user who completed the run
        boss_id: ID of the boss (e.g. 'boss-reactor-core')
        difficulty: Difficulty tier ('normal' | 'hard')
        score: Final score from rubric evaluation
        passed: Whether the boss was defeated
        integrity_delta: HP change (+/-)
        xp_awarded: XP rewarded
    """
    run = BossRun(
        user_id=user_id,
        boss_id=boss_id,
        difficulty=difficulty,
        score=score,
        passed=passed,
        integrity_delta=integrity_delta,
        xp_awarded=xp_awarded,
    )
    session.add(run)
    await session.commit()

from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .models import BossCodexProgress, Profile, BossDefinition

TIER_MAX = 3

async def get_or_create_progress(session: AsyncSession, profile_id: int, boss_id: str) -> BossCodexProgress:
    stmt = select(BossCodexProgress).where(
        BossCodexProgress.profile_id == profile_id,
        BossCodexProgress.boss_id == boss_id
    )
    result = await session.exec(stmt)
    progress = result.first()
    
    if progress is None:
        progress = BossCodexProgress(
            profile_id=profile_id,
            boss_id=boss_id,
            tier_unlocked=0,
            deaths=0,
            wins=0,
            first_seen_at=datetime.utcnow(),
        )
        session.add(progress)
        # We need to flush to get an ID if needed, but for now just adding is enough
    return progress


async def on_boss_failure(session: AsyncSession, profile: Profile, boss_def: BossDefinition):
    progress = await get_or_create_progress(session, profile.id, boss_def.id)

    progress.deaths += 1
    progress.updated_at = datetime.utcnow()

    # Tier unlock logic:
    # Tier 1: first failure (or just seeing it? User said "first encounter or first death")
    # Let's say first death unlocks Tier 1 if not already.
    if progress.deaths >= 1 and progress.tier_unlocked < 1:
        progress.tier_unlocked = 1

    # Tier 2: multiple failures (e.g. 3)
    if progress.deaths >= 3 and progress.tier_unlocked < 2:
        progress.tier_unlocked = 2
        
    session.add(progress)
    await session.commit()


async def on_boss_success(session: AsyncSession, profile: Profile, boss_def: BossDefinition):
    progress = await get_or_create_progress(session, profile.id, boss_def.id)

    progress.wins += 1
    progress.updated_at = datetime.utcnow()
    
    if not progress.first_kill_at:
        progress.first_kill_at = datetime.utcnow()

    # Tier 3: first victory
    if progress.tier_unlocked < 3:
        progress.tier_unlocked = 3
        
    session.add(progress)
    await session.commit()

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Profile, BossDefinition, BossRun, QuestProgress, QuestDefinition, QuestState

@dataclass
class BossTriggerContext:
    profile: Profile
    world_id: str
    track_id: str
    quest_id: str
    was_boss: bool
    passed: bool
    grade: Optional[str] = None  # e.g. "A", "B", "C"
    attempts_on_track: int = 0
    completed_quests_on_track: int = 0

# Simple config for now; you can move this to manifest / DB later.
BOSS_TRIGGER_CONFIG = {
    "default": {
        "min_completed_quests": 3,
        "chance_after_min": 0.25,  # 25% after threshold
        "requires_grade_in": ["A", "B"],
        "cooldown_quests": 2,  # require N normal quests between bosses
    }
}




async def maybe_trigger_boss(ctx: BossTriggerContext, session: Optional[AsyncSession] = None) -> Optional[BossDefinition]:
    cfg = BOSS_TRIGGER_CONFIG["default"]

    # never chain inside a boss
    if ctx.was_boss:
        return None

    # only on success
    if not ctx.passed:
        return None

    # must have enough “normal” progress
    if ctx.completed_quests_on_track < cfg["min_completed_quests"]:
        return None

    # optional grade gate
    if cfg["requires_grade_in"] and ctx.grade not in cfg["requires_grade_in"]:
        return None

    # cooldown: don't trigger if they just had a boss on this track
    # We need to pass session to _cooldown_ok too if we want to reuse it
    if not await _cooldown_ok(ctx.profile, ctx.track_id, cfg["cooldown_quests"], session):
        return None

    # RNG gate
    rng = random.random()
    # print(f"DEBUG: RNG={rng}, Threshold={cfg['chance_after_min']}")
    if rng > cfg["chance_after_min"]:
        # print("DEBUG: RNG check failed")
        return None

    from .database import get_session
    from sqlmodel import select
    from sqlmodel.ext.asyncio.session import AsyncSession

    if session:
        statement = select(BossDefinition).where(
            BossDefinition.world_id == ctx.world_id,
            BossDefinition.track_id == ctx.track_id,
            BossDefinition.enabled == True
        )
        results = await session.exec(statement)
        return results.first()
    else:
        async for session in get_session():
            statement = select(BossDefinition).where(
                BossDefinition.world_id == ctx.world_id,
                BossDefinition.track_id == ctx.track_id,
                BossDefinition.enabled == True
            )
            results = await session.exec(statement)
            return results.first()
    return None


async def _cooldown_ok(profile: Profile, track_id: str, cooldown_quests: int, session: Optional[AsyncSession] = None) -> bool:
    from .database import get_session
    from sqlmodel import select, desc
    from sqlmodel.ext.asyncio.session import AsyncSession
    
    async def check(s: AsyncSession):
        # Find last boss encounter for this track
        boss_stmt = (
            select(BossRun)
            .join(BossDefinition)
            .where(BossRun.user_id == profile.user_id, BossDefinition.track_id == track_id)
            .order_by(desc(BossRun.started_at))
        )
        last_boss = (await s.exec(boss_stmt)).first()
        
        if not last_boss:
            return True

        # Count normal quests since then
        quest_stmt = (
            select(QuestProgress)
            .join(QuestDefinition)
            .where(
                QuestProgress.user_id == profile.user_id,
                QuestDefinition.track_id == track_id,
                QuestProgress.state.in_([QuestState.COMPLETED, QuestState.MASTERED]),
                QuestProgress.completed_at > last_boss.started_at
            )
        )
        normal_since = len((await s.exec(quest_stmt)).all())
        
        return normal_since >= cooldown_quests

    if session:
        return await check(session)
    else:
        async for s in get_session():
            return await check(s)
    return True

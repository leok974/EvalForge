from typing import List, Dict
from sqlmodel import select
from datetime import datetime
from pydantic import BaseModel
from ..database import get_session, AsyncSession
from ..models import BossRun, Profile, QuestProgress, QuestState, QuestDefinition, BossDefinition
from .constants import SENIOR_TRACK_IDS_BY_WORLD, SENIOR_BOSS_IDS

class SeniorWorldProgress(BaseModel):
    world_slug: str
    world_title: str
    senior_track_id: str | None
    senior_quests_total: int
    senior_quests_completed: int
    senior_boss_id: str | None
    senior_boss_cleared: bool


class SeniorProgressResponse(BaseModel):
    worlds: List[SeniorWorldProgress]
    total_senior_bosses: int
    senior_bosses_cleared: int
    legendary_trials_completed: int
    updated_at: datetime


async def get_senior_progress(
    session: AsyncSession,
    profile: Profile,
    worlds: List[Dict], # Passed to avoid import cycles / DB query
) -> SeniorProgressResponse:
    
    # Quest runs and boss runs for this profile
    quest_runs = (
        await session.exec(
            select(QuestProgress).where(
                QuestProgress.user_id == profile.user_id,
                QuestProgress.state.in_([QuestState.COMPLETED, QuestState.MASTERED]),
            )
        )
    ).all()

    boss_runs = (
        await session.exec(
            select(BossRun).where(BossRun.user_id == profile.user_id)
        )
    ).all()
    
    completed_quest_ids = {str(qr.quest_id) for qr in quest_runs}
    
    cleared_boss_ids = {
        br.boss_id for br in boss_runs if br.result == "win"
    }

    legendary_trials_completed = sum(
        1 for br in boss_runs if br.boss_id in SENIOR_BOSS_IDS and br.result == "win"
    )

    senior_worlds: list[SeniorWorldProgress] = []

    # Fetch all quests and bosses to map them
    all_quests = (await session.exec(select(QuestDefinition))).all()
    quests_by_track = {}
    for q in all_quests:
        quests_by_track.setdefault(q.track_id, []).append(q)

    all_bosses = (await session.exec(select(BossDefinition))).all()
    bosses_by_track = {}
    for b in all_bosses:
        bosses_by_track.setdefault(b.track_id, []).append(b)

    for w in worlds:
        w_id = w.get("id")
        w_title = w.get("title", w_id)
        
        senior_track_id = SENIOR_TRACK_IDS_BY_WORLD.get(w_id)
        # Note: We don't have TrackDefinition to verify existence, relying on constant.

        if not senior_track_id:
            senior_worlds.append(
                SeniorWorldProgress(
                    world_slug=w_id,
                    world_title=w_title,
                    senior_track_id=None,
                    senior_quests_total=0,
                    senior_quests_completed=0,
                    senior_boss_id=None,
                    senior_boss_cleared=False,
                )
            )
            continue

        quests = quests_by_track.get(senior_track_id, [])
        senior_quests_total = len(quests)
        senior_quests_completed = sum(
            1 for q in quests if str(q.id) in completed_quest_ids or q.id in completed_quest_ids
        )

        senior_boss_id = None
        senior_boss_cleared = False
        
        track_bosses = bosses_by_track.get(senior_track_id, [])
        if track_bosses:
            senior_boss = track_bosses[-1]
            senior_boss_id = senior_boss.id
            senior_boss_cleared = senior_boss_id in cleared_boss_ids

        senior_worlds.append(
            SeniorWorldProgress(
                world_slug=w_id,
                world_title=w_title,
                senior_track_id=senior_track_id,
                senior_quests_total=senior_quests_total,
                senior_quests_completed=senior_quests_completed,
                senior_boss_id=senior_boss_id,
                senior_boss_cleared=senior_boss_cleared,
            )
        )

    total_senior_bosses = len(SENIOR_BOSS_IDS)
    senior_bosses_cleared = len(SENIOR_BOSS_IDS & cleared_boss_ids)

    return SeniorProgressResponse(
        worlds=senior_worlds,
        total_senior_bosses=total_senior_bosses,
        senior_bosses_cleared=senior_bosses_cleared,
        legendary_trials_completed=legendary_trials_completed,
        updated_at=datetime.utcnow(),
    )

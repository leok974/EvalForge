from typing import List
from fastapi import APIRouter, Depends, Query, Request, HTTPException
from sqlmodel import select
from datetime import datetime
from pydantic import BaseModel
from ..database import AsyncSession, get_session
from ..auth_helper import get_current_user
from ..models import BossRun, BossDefinition, Profile # Removed TrackDefinition/WorldDefinition if not needed/present
from ..practice.constants import SENIOR_BOSS_IDS


class SeniorBossRun(BaseModel):
  boss_id: str
  boss_title: str
  world_slug: str | None
  world_title: str | None
  track_id: str | None
  score: int
  integrity: float
  passed: bool
  created_at: datetime


class SeniorBossRunsResponse(BaseModel):
  items: List[SeniorBossRun]


router = APIRouter(prefix="/api/boss_runs", tags=["boss_runs"])


@router.get("/senior", response_model=SeniorBossRunsResponse)
async def senior_boss_runs(
    request: Request,
    session: AsyncSession = Depends(get_session),
    limit: int = Query(50, ge=1, le=200),
):
    user_dict = await get_current_user(request)
    if not user_dict:
        raise HTTPException(status_code=401, detail="Not authenticated")

    profile_stmt = select(Profile).where(Profile.user_id == user_dict["id"])
    profile = (await session.exec(profile_stmt)).first()
    if not profile:
        return SeniorBossRunsResponse(items=[])

    stmt = (
        select(BossRun, BossDefinition)
        .join(BossDefinition, BossRun.boss_id == BossDefinition.id)
        .where(
            BossRun.user_id == profile.user_id,
            BossRun.boss_id.in_(SENIOR_BOSS_IDS),
        )
        .order_by(BossRun.completed_at.desc())
        .limit(limit)
    )

    results = (await session.exec(stmt)).all()

    # Import worlds to resolve titles
    from ..agent import WORLDS
    
    items: list[SeniorBossRun] = []
    for run, boss in results:
        # Resolve World Title
        w_id = boss.world_id
        w_title = w_id
        if w_id and w_id in WORLDS:
            w_title = WORLDS[w_id].get("title", w_id)

        items.append(
            SeniorBossRun(
                boss_id=run.boss_id,
                boss_title=boss.name or run.boss_id,
                world_slug=w_id,
                world_title=w_title,
                track_id=boss.track_id, # Linking via BossDefinition
                score=getattr(run, "score", 0),
                integrity=float(getattr(run, "hp_remaining", 0.0) or 0.0),
                passed=(run.result == "win"),
                created_at=run.completed_at or datetime.utcnow(),
            )
        )

    return SeniorBossRunsResponse(items=items)

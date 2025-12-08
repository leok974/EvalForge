# arcade_app/routers/routes_boss_qa_worlds.py
"""
Dev-only API routes for standard world boss QA.
Provides endpoint to test all core world bosses (Reactor Core, Signal Prism, etc.).
"""
from __future__ import annotations

from typing import Dict

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from arcade_app.boss_qa_worlds import WorldBossQAReport, WorldBossQARequest, run_standard_world_boss_qa
from arcade_app.database import get_session
from arcade_app.models import Profile
from arcade_app.auth_helper import get_dev_profile_for_boss_qa


router = APIRouter(
    prefix="/api/dev/boss_qa",
    tags=["dev-boss-qa-worlds"],
)


@router.post("/worlds", response_model=WorldBossQAReport)
async def run_world_boss_qa_route(
    request: WorldBossQARequest | None = None,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_dev_profile_for_boss_qa),
) -> WorldBossQAReport:
    """
    Dev-only endpoint: run QA for all standard world bosses (Reactor Core, Signal Prism, etc.).
    """
    # Use the injected AsyncSession
    from sqlmodel import select
    
    try:
        # Check explicit Profile.user_id match
        stmt = select(Profile).where(Profile.user_id == current_user["id"])
        result = await session.exec(stmt)
        profile = result.first()
        
        if not profile:
            profile = Profile(
                user_id=current_user["id"],
                integrity=100,
                total_xp=0,
                global_level=1,
                flags={}
            )
            session.add(profile)
            await session.commit()
            await session.refresh(profile)
        
        min_scores: Dict[str, int] = {}
        report = await run_standard_world_boss_qa(db=session, player=profile, min_scores=min_scores, request=request)
        
        return report
    except Exception as e:
        raise e

# arcade_app/routers/routes_boss_qa_worlds.py
"""
Dev-only API routes for standard world boss QA.
Provides endpoint to test all core world bosses (Reactor Core, Signal Prism, etc.).
"""
from __future__ import annotations

from typing import Dict

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from arcade_app.boss_qa_worlds import WorldBossQAReport, run_standard_world_boss_qa
from arcade_app.database import get_session
from arcade_app.models import Profile
from arcade_app.auth_helper import get_dev_profile_for_boss_qa


router = APIRouter(
    prefix="/api/dev/boss_qa",
    tags=["dev-boss-qa-worlds"],
)


@router.post("/worlds", response_model=WorldBossQAReport)
async def run_world_boss_qa_route(
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_dev_profile_for_boss_qa),
) -> WorldBossQAReport:
    """
    Dev-only endpoint: run QA for all standard world bosses (Reactor Core, Signal Prism, etc.).
    """
    # Create sync session for QA helper
    from sqlalchemy.orm import Session
    from sqlalchemy import create_engine
    import os
    
    sync_db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://evalforge:evalforge@localhost:5432/evalforge")
    sync_db_url = sync_db_url.replace("+asyncpg", "")
    sync_engine = create_engine(sync_db_url)
    sync_session = Session(sync_engine)
    
    try:
        profile = sync_session.query(Profile).filter(Profile.id == current_user["id"]).first()
        if not profile:
            profile = Profile(
                id=current_user["id"],
                display_name=current_user.get("name", "Test User"),
                integrity=100,
                xp=0,
                level=1,
                flags={}
            )
            sync_session.add(profile)
            sync_session.commit()
        
        min_scores: Dict[str, int] = {}
        report = run_standard_world_boss_qa(db=sync_session, player=profile, min_scores=min_scores)
        
        return report
    finally:
        sync_session.close()

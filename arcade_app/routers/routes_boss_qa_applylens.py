"""
Dev-only API routes for ApplyLens boss QA.
Provides a single endpoint to run structured evaluations of both bosses.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from arcade_app.boss_qa_applylens import (
    ApplyLensBossQAReport,
    run_applylens_boss_qa,
)
from arcade_app.database import get_session
from arcade_app.models import Profile
from arcade_app.auth_helper import get_dev_profile_for_boss_qa


router = APIRouter(
    prefix="/api/dev/boss_qa",
    tags=["dev-boss-qa"],
)


@router.post("/applylens", response_model=ApplyLensBossQAReport)
async def run_applylens_boss_qa_route(
    min_score_runtime: int = 60,
    min_score_agent: int = 60,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_dev_profile_for_boss_qa),
) -> ApplyLensBossQAReport:
    """
    Dev-only endpoint: run a full QA pass for ApplyLens bosses (runtime + agent).

    Returns a structured report including scores, grades, HP/integrity deltas, and pass/fail.
    """
    # Get or create a test profile for QA
    # Note: boss_qa_applylens expects a sync session, so we need to adapt
    # For now, create a simple sync session from the async one
    from sqlalchemy.orm import Session
    from sqlalchemy import create_engine
    import os
    
    # Create a sync engine for QA (temporary workaround)
    sync_db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://evalforge:evalforge@localhost:5432/evalforge")
    sync_db_url = sync_db_url.replace("+asyncpg", "")  # Remove async driver
    sync_engine = create_engine(sync_db_url)
    sync_session = Session(sync_engine)
    
    try:
        profile = sync_session.query(Profile).filter(Profile.id == current_user["id"]).first()
        if not profile:
            # Create a test profile
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
        
        report = run_applylens_boss_qa(
            db=sync_session,
            player=profile,
            min_score_runtime=min_score_runtime,
            min_score_agent=min_score_agent,
        )
        
        return report
    finally:
        sync_session.close()

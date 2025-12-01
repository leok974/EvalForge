from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from arcade_app.auth_helper import get_current_user
from arcade_app.boss_helper import (
    create_encounter, get_active_encounter, resolve_boss_attempt
)
from arcade_app.grading_helper import judge_boss_submission
from arcade_app.database import get_session
from arcade_app.models import BossDefinition
from sqlmodel import select

router = APIRouter(prefix="/api/boss", tags=["boss"])

class BossAcceptRequest(BaseModel):
    boss_id: str

class BossSubmitRequest(BaseModel):
    encounter_id: int
    code: str   # or answer payload

@router.get("/current")
async def get_current_boss(user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    enc = await get_active_encounter(user["id"])
    if not enc:
        return {"active": False}
    
    # Fetch Boss Definition for details
    async for session in get_session():
        boss = await session.get(BossDefinition, enc.boss_id)
        return {
            "active": True,
            "encounter_id": enc.id,
            "boss_id": enc.boss_id,
            "expires_at": enc.expires_at.isoformat(),
            "status": enc.status,
            "attempts": enc.attempts,
            "last_score": enc.last_score,
            "technical_objective": boss.technical_objective if boss else "",
            "starting_code": boss.starting_code if boss else ""
        }
    
    return {"active": False} # Should not happen if enc exists

@router.post("/accept")
async def accept_boss(req: BossAcceptRequest, user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    enc = await create_encounter(user["id"], req.boss_id)
    return {
        "encounter_id": enc.id,
        "expires_at": enc.expires_at.isoformat(),
    }

@router.post("/submit")
async def submit_boss(req: BossSubmitRequest, user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Use JudgeAgent / ZERO to score this attempt
    score = await judge_boss_submission(
        user_id=user["id"], encounter_id=req.encounter_id, code=req.code
    )

    enc, status = await resolve_boss_attempt(user["id"], req.encounter_id, score)
    
    return {
        "status": status,
        "score": enc.last_score,
    }


@router.get("/history")
async def get_boss_history(
    limit: int = 5,
    user=Depends(get_current_user),
):
    """
    Get the last N boss runs for the current user.
    Returns boss name, difficulty, score, passed, HP delta, XP, timestamp.
    """
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    from arcade_app.models import BossRun
    from datetime import datetime
    
    async for session in get_session():
        # Query BossRun with JOIN to BossDefinition
        stmt = (
            select(BossRun, BossDefinition.title, BossDefinition.difficulty)
            .join(BossDefinition, BossDefinition.id == BossRun.boss_id)
            .where(BossRun.user_id == user["id"])
            .order_by(BossRun.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(stmt)
        rows = result.all()
        
        history = []
        for run, boss_name, difficulty in rows:
            history.append({
                "boss_id": run.boss_id,
                "boss_name": boss_name,
                "difficulty": difficulty,
                "score": run.score,
                "passed": run.passed,
                "integrity_delta": run.integrity_delta,
                "xp_awarded": run.xp_awarded,
                "created_at": run.created_at.isoformat(),
            })
        
        return history
    
    return []

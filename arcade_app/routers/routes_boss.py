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
            "status": "active",
            "attempts": 1, # Placeholder
            "last_score": 0, # Placeholder
            "technical_objective": boss.technical_objective if boss else "",
            "starting_code": boss.starting_code if boss else "",
            "hp_remaining": enc.hp_remaining
        }
    
    return {"active": False} # Should not happen if enc exists

@router.post("/accept")
async def accept_boss(req: BossAcceptRequest, user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    enc = await create_encounter(user["id"], req.boss_id)
    
    # FX: Boss Spawn
    from arcade_app.socket_manager import emit_fx_event
    await emit_fx_event(user["id"], {
        "type": "boss_spawn",
        "boss_id": enc.boss_id,
        "severity": "high",
    })
    
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
    
    # FX: Boss Result
    from arcade_app.socket_manager import emit_fx_event
    if status == "win":
        await emit_fx_event(user["id"], {
            "type": "boss_result",
            "outcome": "success",
            "xp": 300, # TODO: fetch real XP from boss def
        })
    else:
        await emit_fx_event(user["id"], {
            "type": "boss_result",
            "outcome": "failure",
            "integrity_loss": 10, # TODO: fetch real penalty
        })
    
    return {
        "status": status,
        "score": enc.score,
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
            select(BossRun, BossDefinition.name, BossDefinition.difficulty)
            .join(BossDefinition, BossDefinition.id == BossRun.boss_id)
            .where(BossRun.user_id == user["id"])
            .order_by(BossRun.started_at.desc())
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
                "passed": run.result == "win",
                "integrity_delta": 0, # Not stored in BossRun yet
                "xp_awarded": 0,      # Not stored in BossRun yet
                "created_at": run.started_at.isoformat(),
            })
        
        return history
    
    return []

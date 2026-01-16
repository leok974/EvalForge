import hashlib
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os

from arcade_app.database import get_session as get_db
# from arcade_app.auth import get_user_id # Need to mock or implement this
from arcade_app.progress_models import QuestAttempt, QuestProgressV2, QuestHintUnlock
from arcade_app.schemas.quest_run import RunRequest, RunResponse
from arcade_app.services.quest_validate import validate_first_sparks_python

router = APIRouter(prefix="/api/quests", tags=["quests-runtime"])

# --- Auth Hack ---
DEV_FAKE_AUTH = os.getenv("DEV_FAKE_AUTH", "1") != "0" # Default true for dev convenience per user request

async def get_user_id(x_dev_user: str | None = Header(default=None)):
    if DEV_FAKE_AUTH:
        return x_dev_user or "dev-user"
    # TODO: real auth (cookie/session/JWT)
    # raise HTTPException(status_code=401, detail="Not authenticated")
    return "dev-user" # Fallback

def sha(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()

async def _get_or_create_progress(db: AsyncSession, user_id: str, quest_id: str) -> QuestProgressV2:
    q = await db.execute(select(QuestProgressV2).where(
        QuestProgressV2.user_id == user_id,
        QuestProgressV2.quest_id == quest_id,
    ))
    row = q.scalar_one_or_none()
    if row:
        return row
    row = QuestProgressV2(user_id=user_id, quest_id=quest_id, status="in_progress")
    db.add(row)
    await db.flush()
    return row

@router.post("/{quest_id}/run", response_model=RunResponse)
async def run_quest(
    quest_id: str,
    payload: RunRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_user_id),
):
    # TODO: lookup quest type/language from DB; for now assume starter quest
    if payload.language != "python":
        raise HTTPException(400, "Only python supported right now")

    objective_results = validate_first_sparks_python(payload.code)
    passed = all(o.get("ok") for o in objective_results if o["id"] != "syntax")

    # Persist attempt + progress
    attempt = QuestAttempt(
        user_id=user_id,
        quest_id=quest_id,
        is_submit=False,
        passed=passed,
        duration_ms=0,
        code=payload.code,
        code_hash=sha(payload.code),
        stdout=None,
        stderr=None,
        objective_results=objective_results,
        meta={"mode": "validate"},
    )
    db.add(attempt)

    prog = await _get_or_create_progress(db, user_id, quest_id)
    prog.runs_count += 1
    prog.attempts_count += 1
    prog.last_run_at = datetime.utcnow()

    await db.commit()

    return {
        "passed": passed,
        "objective_results": objective_results,
        "stdout": None,
        "stderr": None,
        "ready_to_submit": passed,
    }

@router.post("/{quest_id}/submit", response_model=dict)
async def submit_quest(
    quest_id: str,
    payload: RunRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_user_id),
):
    objective_results = validate_first_sparks_python(payload.code)
    passed = all(o.get("ok") for o in objective_results if o["id"] != "syntax")
    if not passed:
        return {"ok": False, "reason": "Objectives not met", "objective_results": objective_results}

    # award XP (simple for now)
    xp_awarded = 50
    mastery_awarded = 0

    attempt = QuestAttempt(
        user_id=user_id,
        quest_id=quest_id,
        is_submit=True,
        passed=True,
        duration_ms=0,
        code=payload.code,
        code_hash=sha(payload.code),
        stdout=None,
        stderr=None,
        objective_results=objective_results,
        meta={"mode": "submit", "xp": xp_awarded},
    )
    db.add(attempt)

    prog = await _get_or_create_progress(db, user_id, quest_id)
    prog.attempts_count += 1
    prog.status = "completed"
    prog.completed_at = datetime.utcnow()
    prog.last_xp = xp_awarded
    prog.best_xp = max(prog.best_xp, xp_awarded)

    await db.commit()

    return {
        "ok": True,
        "quest_id": quest_id,
        "xp_awarded": xp_awarded,
        "mastery_awarded": mastery_awarded,
        "objective_results": objective_results,
        "status": "completed",
    }

@router.post("/{quest_id}/hints/unlock", response_model=dict)
async def unlock_hints(
    quest_id: str,
    tier: int,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_user_id),
):
    if tier not in (1,2,3):
        raise HTTPException(400, "tier must be 1..3")

    prog = await _get_or_create_progress(db, user_id, quest_id)

    # simple gating: require >= tier runs
    if prog.runs_count < tier:
        return {"ok": False, "reason": f"Need {tier} runs to unlock tier {tier}", "runs": prog.runs_count}

    q = await db.execute(select(QuestHintUnlock).where(
        QuestHintUnlock.user_id == user_id,
        QuestHintUnlock.quest_id == quest_id,
    ))
    unlock = q.scalar_one_or_none()
    if not unlock:
        unlock = QuestHintUnlock(user_id=user_id, quest_id=quest_id, max_tier=0)
        db.add(unlock)
        await db.flush()

    unlock.max_tier = max(unlock.max_tier, tier)
    prog.hint_tier_unlocked = max(prog.hint_tier_unlocked, tier)

    await db.commit()
    return {"ok": True, "quest_id": quest_id, "max_tier": unlock.max_tier}

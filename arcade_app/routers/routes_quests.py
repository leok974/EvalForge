
from typing import List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from pydantic import BaseModel
from datetime import datetime

from arcade_app.database import get_session
from arcade_app.auth_helper import get_current_user
from arcade_app.models import QuestDefinition, QuestState, Profile
from arcade_app.progress_models import QuestProgressV2, QuestAttempt
from arcade_app.quest_helper import quest_to_dict
# from arcade_app.services.quest_validate import validate_first_sparks_with_runtime # We'll need this or generic runner

router = APIRouter(prefix="/api/quests", tags=["quests"])

# Helper to map V2 status to QuestState
def map_status_to_state(status: str) -> str:
    # V2 status: locked, available, in_progress, completed, mastered
    # QuestState: same values mostly
    return status

@router.get("/", response_model=List[Dict])
async def list_quests(
    world_id: Optional[str] = None,
    session: Session = Depends(get_session),
    user_data: Dict = Depends(get_current_user),
):
    if not user_data:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_id = user_data["id"]
    # Ensure profile exists
    result = await session.exec(select(Profile).where(Profile.user_id == user_id))
    profile = result.first()
    if not profile:
        profile = Profile(user_id=user_id)
        session.add(profile)
        await session.commit()
        await session.refresh(profile)

    query = select(QuestDefinition)
    if world_id:
        query = query.where(QuestDefinition.world_id == world_id)
    
    query = query.order_by(
        QuestDefinition.world_id,
        QuestDefinition.track_id,
        QuestDefinition.order_index
    )
    
    result = await session.exec(query)
    quests = result.all()
    
    # Fetch progress V2 using slugs
    quest_slugs = [q.slug for q in quests]
    progress_stmt = select(QuestProgressV2).where(
        QuestProgressV2.user_id == user_id,
        QuestProgressV2.quest_id.in_(quest_slugs)
    )
    result = await session.exec(progress_stmt)
    progress_entries = result.all()
    progress_map = {p.quest_id: p for p in progress_entries}
    
    # We need to adapt the quest_to_dict helper or inline it if it expects legacy QuestProgress
    # Assuming quest_to_dict expects an object with 'state' attribute.
    # QuestProgressV2 has 'status'. We can wrap it or mock it.
    
    results = []
    for q in quests:
        prog = progress_map.get(q.slug)
        # Adapt V2 to interface expected by quest_to_dict (dummy object)
        qp_wrapper = None
        if prog:
            class Wrapper:
                state = prog.status
                attempts = prog.attempts_count
                best_score = float(prog.best_xp) # abusing field for simple view
            qp_wrapper = Wrapper()
        
        results.append(quest_to_dict(q, qp_wrapper))

    return results


@router.get("/{quest_slug}", response_model=Dict)
async def get_quest(
    quest_slug: str,
    session: Session = Depends(get_session),
    user_data: Dict = Depends(get_current_user),
):
    if not user_data:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    user_id = user_data["id"]
    # Profile check omitted for brevity, implied by list/auth
    
    result = await session.exec(select(QuestDefinition).where(QuestDefinition.slug == quest_slug))
    quest = result.first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
        
    # Fetch progress V2
    result = await session.exec(
        select(QuestProgressV2).where(
            QuestProgressV2.user_id == user_id,
            QuestProgressV2.quest_id == quest_slug
        )
    )
    prog = result.first()
    
    qp_wrapper = None
    if prog:
        class Wrapper:
            state = prog.status
            attempts = prog.attempts_count
            best_score = float(prog.best_xp)
        qp_wrapper = Wrapper()
    
    return quest_to_dict(quest, qp_wrapper)


@router.post("/{quest_slug}/accept", response_model=Dict)
async def accept_quest(
    quest_slug: str,
    session: Session = Depends(get_session),
    user_data: Dict = Depends(get_current_user),
):
    if not user_data:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    user_id = user_data["id"]
    
    result = await session.exec(select(QuestDefinition).where(QuestDefinition.slug == quest_slug))
    quest = result.first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
        
    # Get or create V2 progress
    result = await session.exec(
        select(QuestProgressV2).where(
            QuestProgressV2.user_id == user_id,
            QuestProgressV2.quest_id == quest_slug
        )
    )
    prog = result.first()
    if not prog:
        prog = QuestProgressV2(
            user_id=user_id,
            quest_id=quest_slug,
            status="in_progress",
            first_started_at=datetime.utcnow()
        )
        session.add(prog)
    else:
        if prog.status in ("locked", "available"):
             prog.status = "in_progress"
             session.add(prog)
             
    await session.commit()
    await session.refresh(prog)
    
    class Wrapper:
        state = prog.status
        attempts = prog.attempts_count
        best_score = 0
    
    return quest_to_dict(quest, Wrapper())


class QuestSubmissionPayload(BaseModel):
    code: str
    language: Optional[str] = None


@router.post("/{quest_slug}/submit", response_model=Dict)
async def submit_quest_solution(
    quest_slug: str,
    payload: QuestSubmissionPayload,
    session: Session = Depends(get_session),
    user_data: Dict = Depends(get_current_user),
):
    """
    Submits the quest solution.
    Runs the code (authoritative run), validates it, persists result, updates XP.
    """
    if not user_data:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    user_id = user_data["id"] 
    # Profile needed for XP
    result = await session.exec(select(Profile).where(Profile.user_id == user_id))
    profile = result.first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    result = await session.exec(select(QuestDefinition).where(QuestDefinition.slug == quest_slug))
    quest = result.first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")

    # 1. Authoritative Execution & Validation
    # We must use the runtime validator.
    from arcade_app.services.quest_validate import validate_quest_attempt
    
    # We assume 'mode=execute'
    from arcade_app.services.code_runner_docker import run_python_docker
    
    # Exec
    run_res_obj = run_python_docker(payload.code, timeout_ms=3000)
    
    # Convert ExecResult to dict for consistency
    run_res = {
        "stdout": run_res_obj.stdout,
        "stderr": run_res_obj.stderr,
        "exit_code": run_res_obj.exit_code,
        "duration_ms": run_res_obj.duration_ms,
        "timed_out": run_res_obj.timed_out
    }
    
    # Validate using Generic Validator (Config-Driven)
    objective_results = validate_quest_attempt(
        code=payload.code,
        stdout=run_res["stdout"],
        stderr=run_res["stderr"],
        exit_code=run_res["exit_code"],
        timed_out=run_res["timed_out"],
        quest_def=quest
    )
    
    # Determine pass/fail
    if not objective_results:
        # Fallback if no objectives defined (rare but possible for simple playground)
        passed = run_res["exit_code"] == 0
        detail = "Run successful" if passed else "Run failed"
        objective_results.append({"id": "execution", "ok": passed, "detail": detail})
    else:
        passed = all(r["ok"] for r in objective_results)

    # 2. Persist Attempt
    attempt = QuestAttempt(
        user_id=user_id,
        quest_id=quest_slug,
        is_submit=True,
        passed=passed,
        duration_ms=run_res.get("duration_ms", 0),
        code=payload.code,
        code_hash="sha-placeholder", # TODO
        stdout=run_res["stdout"],
        stderr=run_res["stderr"],
        objective_results=objective_results,
        meta={"exit_code": run_res["exit_code"]}
    )
    session.add(attempt)
    
    # 3. Update Progress V2
    result = await session.exec(select(QuestProgressV2).where(QuestProgressV2.user_id == user_id, QuestProgressV2.quest_id == quest_slug))
    prog = result.first()
    if not prog:
        prog = QuestProgressV2(user_id=user_id, quest_id=quest_slug, status="in_progress")
        session.add(prog)
        
    prog.attempts_count += 1
    prog.runs_count += 1
    prog.last_run_at = datetime.utcnow()
    
    xp_awarded = 0
    prev_status = prog.status
    
    if passed:
        prog.status = "completed" # or mastered if bonus criteria?
        prog.completed_at = datetime.utcnow()
        
        # XP Logic
        # Simple: Award base if not already completed
        if prev_status not in ("completed", "mastered"):
            xp_awarded = quest.base_xp_reward
            prog.best_xp = max(prog.best_xp, xp_awarded)
            prog.last_xp = xp_awarded
            
            # Profile XP
            profile.total_xp = (profile.total_xp or 0) + xp_awarded
            session.add(profile)
            
    session.add(prog)
    await session.commit()
    await session.refresh(attempt)
    await session.refresh(prog)
    await session.refresh(profile)

    class Wrapper:
        state = prog.status
        attempts = prog.attempts_count
        best_score = float(prog.best_xp)

    return {
        "quest": quest_to_dict(quest, Wrapper()),
        "score": 100 if passed else 0,
        "passed": passed,
        "xp_awarded": xp_awarded,
        "unlock_events": [], # TODO
        "profile": {
            "xp": profile.total_xp,
            "flags": profile.flags,
        },
        "attempt_id": str(attempt.id)
    }

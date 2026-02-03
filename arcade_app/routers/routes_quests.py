
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
from arcade_app.services.quest_validate import validate_first_sparks_with_runtime # We'll need this or generic runner
from arcade_app.services.security import sanitize_logs
from arcade_app.services.utils import build_effective_workspace
from arcade_app.services.quick_fix_generator import generate_quick_fixes

router = APIRouter(prefix="/api/quests", tags=["quests"])

# Helper to map V2 status to QuestState
def map_status_to_state(status: str) -> str:
    # V2 status: locked, available, in_progress, completed, mastered
    # QuestState: same values mostly
    return status

@router.get("", response_model=List[Dict])
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

    query = select(QuestDefinition).where(QuestDefinition.is_archived == False)
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
    
    # Logic to determine availability for quests without progress
    # Group by track and sort by order
    quests_by_track = {}
    for q in quests:
        if q.track_id not in quests_by_track:
            quests_by_track[q.track_id] = []
        quests_by_track[q.track_id].append(q)

    # Determine state override
    calculated_states = {} # slug -> state override
    
    for track_id, track_quests in quests_by_track.items():
        # Assumes track_quests are already sorted by order_index from the query
        previous_completed = True # First quest is available if there are no prereqs (implied by order)
        
        for q in track_quests:
            prog = progress_map.get(q.slug)
            
            # If we have progress, that state is the truth
            if prog:
                is_done = prog.status in ("completed", "mastered")
                previous_completed = is_done
                continue
            
            # No progress: Check if it should be available
            if previous_completed:
                calculated_states[q.slug] = "available"
                previous_completed = False
            else:
                calculated_states[q.slug] = "locked"
                previous_completed = False

    class QuestProgressWrapper:
        def __init__(self, state, attempts=0, best_score=0, hint_tier_unlocked=0):
            self.state = state
            self.attempts = attempts
            self.best_score = best_score
            self.hint_tier_unlocked = hint_tier_unlocked

    results = []
    for q in quests:
        prog = progress_map.get(q.slug)
        qp_wrapper = None
        
        if prog:
            qp_wrapper = QuestProgressWrapper(
                state=prog.status,
                attempts=prog.attempts_count,
                best_score=float(prog.best_xp or 0),
                hint_tier_unlocked=prog.hint_tier_unlocked
            )
        elif q.slug in calculated_states:
             qp_wrapper = QuestProgressWrapper(
                state=calculated_states[q.slug]
             )
        
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
            hint_tier_unlocked = prog.hint_tier_unlocked
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
    workspace: Optional[List[Dict]] = None


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
    run_workspace = None
    workspace_def = getattr(quest, "workspace_json", None)
    if workspace_def:
         run_workspace = build_effective_workspace(workspace_def, payload.workspace or [])

    run_res_obj = run_python_docker(payload.code, timeout_ms=3000, workspace=run_workspace)
    
    # Sanitize
    run_res_obj.stdout = sanitize_logs(run_res_obj.stdout)
    run_res_obj.stderr = sanitize_logs(run_res_obj.stderr)
    
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
        workspace_snapshot_json=[f for f in run_workspace.get("files", []) if f.get("editable", True)] if run_workspace else None,
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
    
    # Stuck Detector Integration
    from arcade_app.services.stuck_detector import update_stuck_progress, generate_coach_response
    
    failure_summary = {}
    if not passed:
        primary = "output_mismatch"
        # Submit execution logic is simpler here, assume run_res has details
        if run_res.get("timed_out"): primary = "timeout"
        elif run_res.get("exit_code") != 0: primary = "runtime_exception"
        failure_summary = {"primary": primary}
        
    update_stuck_progress(prog, passed, is_submit=True, failure_summary=failure_summary)
    coach_data = generate_coach_response(prog, failure_summary)
    
    xp_awarded = 0
    prev_status = prog.status
    
    debrief_data = None
    diagnostics_data = []
    
    # Phase 7.1.3: Inline Diagnostics
    if not passed or (run_res.get("stderr") and len(run_res.get("stderr", "") ) > 0):
        from arcade_app.services.diagnostics_parser import parse_diagnostics
        
        # Get workspace files from payload
        workspace_paths = []
        if payload.workspace and "files" in payload.workspace:
             workspace_paths = [f["path"] for f in payload.workspace["files"]]
             
        diagnostics_data = parse_diagnostics(
            run_res.get("stderr", ""),
            payload.language,
            workspace_paths
        )
        
        diagnostics_data = parse_diagnostics(
            run_res.get("stderr", ""),
            payload.language,
            workspace_paths
        )
        
    attempt.diagnostics_json = diagnostics_data

    # Phase 7.1.4: Quick Fixes
    # Reconstruct workspace for generator
    gen_workspace = {}
    if run_workspace and "files" in run_workspace:
        for f in run_workspace["files"]:
            # Use content from run_workspace (merged)
            gen_workspace[f["path"]] = {"content": f.get("content", "")}
    elif payload.workspace:
         # Fallback to payload if run_workspace failed?
         # payload.workspace is list of dicts {path, content}
         if isinstance(payload.workspace, list): # It's defined as List[Dict] in schema
             for f in payload.workspace:
                 gen_workspace[f.get("path")] = {"content": f.get("content", "")}
    
    q_fixes = generate_quick_fixes(
        language=payload.language or "python",
        failure_summary=failure_summary,
        diagnostics=diagnostics_data, 
        objective_results=objective_results,
        workspace_snapshot=gen_workspace,
        hidden_tests_reveal=False # Submit never reveals hidden details
    )
    attempt.quick_fixes_json = [f.model_dump() for f in q_fixes]

    if passed:
        prog.status = "completed" # or mastered if bonus criteria?
        if not prog.completed_at:
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

        # Success Debrief (Phase 7.1.2)
        # Import inside to avoid circular deps if any
        from arcade_app.services.debrief_generator import generate_debrief
        debrief_data = await generate_debrief(session, quest, attempt, prog)
        attempt.debrief_json = debrief_data
            
    session.add(prog)
    await session.commit()
    await session.refresh(attempt)
    await session.refresh(prog)
    await session.refresh(profile)

    return {
        "passed": passed,
        "message": "Quest Completed!" if passed else "Keep trying!",
        "xp_awarded": xp_awarded,
        "new_status": prog.status,
        "objective_results": objective_results,
        "coach": coach_data,
        "debrief": debrief_data,
        "diagnostics": diagnostics_data,
        "quick_fixes": [f.model_dump() for f in q_fixes]
    }



@router.get("/{quest_id}/attempts/{attempt_id}/report", response_model=Dict)
async def get_attempt_report(
    quest_id: str,
    attempt_id: str,
    format: str = "json", # json | md
    session: Session = Depends(get_session),
    user_data: Dict = Depends(get_current_user),
):
    """
    Returns a sanitized report of the attempt.
    """
    if not user_data:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    user_id = user_data["id"] 
    # Get attempt
    attempt = await session.exec(select(QuestAttempt).where(
        QuestAttempt.id == attempt_id,
        QuestAttempt.user_id == user_id
    ))
    attempt = attempt.first()
    if not attempt:
        raise HTTPException(404, "Attempt not found")
        
    # Get quest
    # (used for titles/context if needed, but attempt has most info)
    quest = await session.exec(select(QuestDefinition).where(QuestDefinition.slug == quest_id))
    quest = quest.first()
        
    # Build Data
    data = {
        "quest_id": quest_id,
        "quest_title": quest.title if quest else quest_id,
        "attempt_id": str(attempt.id),
        "run_number": attempt.meta.get("seq") or attempt.meta.get("run_number") or 0,
        "created_at": attempt.created_at.isoformat(),
        "passed": attempt.passed,
        "duration_ms": attempt.duration_ms,
        "exit_code": attempt.meta.get("exit_code"),
        "timed_out": attempt.meta.get("timed_out", False),
        "stdout": sanitize_logs(attempt.stdout), # re-sanitize to be safe
        "stderr": sanitize_logs(attempt.stderr),
        "objectives": attempt.objective_results,
    }
    
    # Snapshot (workspace) - ONLY EDITABLE FILES
    # Attempt stores valid workspace snapshot?
    # Schema check: QuestAttempt has workspace_snapshot_json?
    # I added it in Phase 6 but didn't verify it's populated in Submit/Run?
    # Wait, I updated Submit/Run to store workspace?
    # Let me check my previous edits or file content.
    # Lines 241-253 in routes_quests.py do NOT populate workspace_snapshot_json!
    # I missed that in Phase 6 implementation for persistence.
    # I should add it now to Submit (Line 241) and Run (routes_quests_runtime.py).
    
    # For now, if missing, return empty or omitted.
    snapshot = attempt.workspace_snapshot_json or []
    # Filter editable only?
    # Assuming snapshot was stored correctly. If not, I can't filter here easily without quest def.
    # But hardening rule A4 says: "workspace_snapshot_json contains editable files only".
    # So I should enforce that AT WRITE TIME.
    
    data["workspace_files"] = snapshot

    if format == "md":
        # Generate Markdown
        md = f"# Run Report: {data['quest_title']} (#{data['run_number']})\n\n"
        md += f"**Date**: {data['created_at']}\n"
        md += f"**Status**: {'✅ PASSED' if data['passed'] else '❌ FAILED'}\n"
        md += f"**Duration**: {data['duration_ms']}ms\n\n"
        
        md += "## Objectives\n"
        for obj in data["objectives"]:
            icon = "✅" if obj["ok"] else "❌"
            md += f"- {icon} **{obj['id']}**: {obj.get('detail') or ''}\n"
            
        md += "\n## Output\n"
        if data["stdout"]:
            md += "### Stdout\n```\n" + data["stdout"] + "\n```\n"
        if data["stderr"]:
            md += "### Stderr\n```\n" + data["stderr"] + "\n```\n"
            
        md += "\n## Workspace (Editable Files)\n"
        for f in data["workspace_files"]:
             md += f"### {f['path']}\n```python\n{f['content']}\n```\n"
             
        return {"report": md}
        
    return data

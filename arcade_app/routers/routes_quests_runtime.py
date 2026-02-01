import hashlib
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os

from arcade_app.database import get_session as get_db
from arcade_app.auth_helper import get_current_user
from arcade_app.progress_models import QuestAttempt, QuestProgressV2, QuestHintUnlock
from arcade_app.schemas.quest_run import RunRequest, RunResponse
from sqlalchemy import desc
from arcade_app.models import QuestDefinition
from arcade_app.services.quest_validate import validate_quest_attempt
from arcade_app.services.security import sanitize_logs
from arcade_app.services.utils import build_effective_workspace
from arcade_app.services.quick_fix_generator import generate_quick_fixes
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/api/quests", tags=["quests-runtime"])

# Phase 8.x PR 3: Idempotency helper
async def get_existing_attempt_by_idempotency(
    db: AsyncSession,
    user_id: str,
    quest_id: str,
    is_submit: bool,
    idempotency_key: str
) -> QuestAttempt | None:
    """
    Check for existing attempt with same idempotency key.
    Returns None if not found or if key is None.
    """
    if not idempotency_key:
        return None
    
    result = await db.execute(
        select(QuestAttempt).where(
            QuestAttempt.user_id == user_id,
            QuestAttempt.quest_id == quest_id,
            QuestAttempt.is_submit == is_submit,
            QuestAttempt.idempotency_key == idempotency_key
        ).order_by(desc(QuestAttempt.created_at))
    )
    return result.scalar_one_or_none()

# Wrapper to get just the ID for runtime routes
async def get_user_id(
    request: Request,
    x_dev_user: str | None = Header(default=None)
) -> str:
    # 1. Try standard auth
    user = await get_current_user(request)
    if user and user.get("id"):
        return user["id"]
        
    # 2. Fallback for pure dev/curl testing if needed
    if os.getenv("DEV_FAKE_AUTH", "1") != "0":
        return x_dev_user or "dev-user"
        
    raise HTTPException(status_code=401, detail="Not authenticated")

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
    # Phase 8.x PR 3: Check for existing attempt with same idempotency key
    existing = await get_existing_attempt_by_idempotency(
        db, user_id, quest_id, is_submit=False, idempotency_key=payload.idempotency_key
    )
    if existing:
        # Return existing result (idempotent - don't re-execute)
        prog = await _get_or_create_progress(db, user_id, quest_id)
        return {
            "passed": existing.passed,
            "objective_results": existing.objective_results,
            "stdout": existing.stdout,
            "stderr": existing.stderr,
            "ready_to_submit": existing.passed and not existing.meta.get("timed_out", False),
            "attempt_id": str(existing.id),
            "run_number": existing.meta.get("seq", prog.runs_count),
            "duration_ms": existing.duration_ms,
            "exit_code": existing.meta.get("exit_code", 0),
            "timed_out": existing.meta.get("timed_out", False),
            "coach": existing.meta.get("coach"),  # May be None
            "debrief": existing.debrief_json if existing.debrief_json else None,
            "diagnostics": existing.diagnostics_json if existing.diagnostics_json else [],
            "quick_fixes": existing.quick_fixes_json if existing.quick_fixes_json else []
        }
    
    # Fetch Quest Def (for validation rules)
    result = await db.execute(select(QuestDefinition).where(QuestDefinition.slug == quest_id))
    quest = result.scalar_one_or_none()
    
    # Fallback for "first-sparks" if not in DB not needed if seeded?
    # validation handles None quest_def gracefully?
    # If quest is None, we might want 404, or generic.
    
    target_language = getattr(quest, "language", "python") if quest else "python"
    
    if payload.language and payload.language != target_language:
         # Be lenient if new quest pack format not fully propagated, OR strict?
         # Strict is better for Phase 5.
         pass
         # raise HTTPException(400, f"Language mismatch. Quest requires {target_language}")
         # Actually let's trust payload or force it?
         # Dispatcher relies on language to pick docker backend.
    
    # Execution Logic
    stdout = stderr = None
    timed_out = False
    duration_ms = 0
    exit_code = 0
    
    EXECUTION_ENABLED = os.getenv("EXECUTION_ENABLED", "0") == "1"
    EXECUTION_TIMEOUT_MS = int(os.getenv("EXECUTION_TIMEOUT_MS", "2000"))
    
    run_workspace = None

    if (payload.mode in ["execute", "tests"]) and EXECUTION_ENABLED:
        from arcade_app.services.code_runner import run_code
        
        # Construct effective workspace if needed
        workspace_def = getattr(quest, "workspace_json", None)
        
        if workspace_def:
             # Merge overlay
             user_overlay = payload.workspace or []
             run_workspace = build_effective_workspace(workspace_def, user_overlay)
        elif payload.workspace:
             # Fallback: Use payload workspace directly if no quest workspace defined
             run_workspace = {"files": payload.workspace}
        
        # Use payload language if provided, else default to python (or quest language)
        lang = payload.language or "python"
        
        # Pass workspace to runner
        r = run_code(lang, payload.code, stdin=getattr(payload, "stdin", "") or "", timeout_ms=EXECUTION_TIMEOUT_MS, workspace=run_workspace, mode=payload.mode if payload.mode == "tests" else "run")
        
        # Sanitize logs
        stdout = sanitize_logs(r.stdout)
        stderr = sanitize_logs(r.stderr)
        timed_out, duration_ms = r.timed_out, r.duration_ms
        exit_code = r.exit_code if r.exit_code is not None else (1 if timed_out else 0)

    # Resolve source code for static analysis (AST/Regex)
    # If payload.code is empty (workspace mode), use the entrypoint file content
    validation_code = payload.code
    # Resolve source code for static analysis (AST/Regex)
    # If payload.code is empty (workspace mode), use the entrypoint file content
    validation_code = payload.code
    
    if not validation_code:
        # 1. Try effective workspace (execution mode)
        target_files = []
        if run_workspace and "files" in run_workspace:
            target_files = run_workspace["files"]
        # 2. Fallback to payload workspace (validate mode)
        elif payload.workspace:
             # payload.workspace is a list of dicts (or objects)
             target_files = payload.workspace

        if target_files:
            # Determine entrypoint
            entry_file = getattr(payload, "entrypoint", None)
            if not entry_file and getattr(quest, "workspace", None):
                entry_file = quest.workspace.get("entrypoint")
            if not entry_file:
                entry_file = "main.py" # Default
            
            # Find content
            for f in target_files:
                # Handle both dict and Pydantic object
                f_path = f.get("path") if isinstance(f, dict) else getattr(f, "path", None)
                if f_path == entry_file:
                    validation_code = f.get("content") if isinstance(f, dict) else getattr(f, "content", "")
                    break

    # Validate
    objective_results = validate_quest_attempt(
        code=validation_code,
        stdout=stdout,
        stderr=stderr,
        exit_code=exit_code,
        timed_out=timed_out,
        quest_def=quest
    )
    
    passed = False
    if objective_results:
        passed = all(o.get("ok") for o in objective_results)
    else:
        # No objectives? Passed if run ok
        if payload.mode == "execute":
            passed = not timed_out
        else:
            pass # AST only? defaults to ok if no checks? 
            # If no quest def, maybe passed=False?
            # Let's verify: Generic validator returns empty list if no rules.
            # If nothing to check, it's a pass?
            passed = True # Optimistic for playground
            
    # Persist attempt + progress

    # Persist attempt + progress
    # Persist attempt + progress
    prog = await _get_or_create_progress(db, user_id, quest_id)
    prog.runs_count += 1
    prog.attempts_count += 1
    prog.last_run_at = datetime.utcnow()
    
    # Stuck Detector Integration
    from arcade_app.services.stuck_detector import update_stuck_progress, generate_coach_response
    
    # Analyze failure
    failure_summary = {}
    if not passed:
        # Simple heuristic for now - assuming phase 7.1 not fully present yet
        # If timed_out -> timeout
        # If exit_code != 0 -> runtime_exception
        # Else -> output_mismatch
        primary = "output_mismatch"
        if timed_out: primary = "timeout"
        elif exit_code != 0: primary = "runtime_exception"
        
        failure_summary = {"primary": primary}
        
    update_stuck_progress(prog, passed, is_submit=False, failure_summary=failure_summary)
    coach_data = generate_coach_response(prog, failure_summary)
    
    # Phase 8.x PR 4: Compute workspace hash + execution context
    from arcade_app.services.workspace_hash import hash_workspace_snapshot, build_execution_context
    
    workspace_hash = hash_workspace_snapshot({
        "entrypoint": getattr(payload, "entrypoint", None) or "main.py",
        "files": run_workspace.get("files", []) if run_workspace else []
    })
    
    execution_context = build_execution_context(
        language=payload.language or "python",
        mode=payload.mode,
        duration_ms=duration_ms,
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
        timed_out=timed_out
    )
    
    attempt = QuestAttempt(
        user_id=user_id,
        quest_id=quest_id,
        is_submit=False,
        passed=passed,
        duration_ms=duration_ms,
        code=payload.code,
        code_hash=sha(payload.code),
        stdout=stdout,
        stderr=stderr,
        objective_results=objective_results,
        meta={
            "mode": "validate" if payload.mode != "execute" else "execute", 
            "timed_out": timed_out,
            "exit_code": exit_code,
            "seq": prog.runs_count
        },
        workspace_snapshot_json=[f for f in run_workspace.get("files", []) if f.get("editable", True)] if run_workspace else None,
        idempotency_key=payload.idempotency_key,  # Phase 8.x PR 3
        workspace_hash=workspace_hash,  # Phase 8.x PR 4
        execution_context_json=execution_context,  # Phase 8.x PR 4
    )
    debrief_data = None
    diagnostics_data = []
    
    # Phase 7.1.3: Inline Diagnostics
    # Parse diagnostics if failed (or even if passed, for warnings?)
    # Usually only relevant if exit_code != 0 or generic error
    if exit_code != 0 or (stderr and len(stderr) > 0):
       from arcade_app.services.diagnostics_parser import parse_diagnostics
       # Gather workspace files from payload or quest def? 
       # payload.workspace has files.
       workspace_paths = []
       if run_workspace and "files" in run_workspace:
           workspace_paths = [f["path"] for f in run_workspace["files"]]
        
       if not workspace_paths and payload.code:
            # Fallback for single file execution
            fname = "main.py"
            if payload.language == "javascript": fname = "main.js"
            elif payload.language == "typescript": fname = "main.ts"
            workspace_paths.append(fname)
       
       # Also include active files if singular?
       # The parser handles cleaning paths.
       
       diagnostics_data = parse_diagnostics(
           stderr or "", 
           payload.language, 
           workspace_paths
       )
       
    attempt.diagnostics_json = diagnostics_data

    # Phase 7.1.4: Quick Fixes
    # Reconstruct workspace for generator (run_workspace has the effective structure)
    # But run_workspace format is dict with "files": [list]. 
    # Generator expects workspace_snapshot dict {path: {content}}.
    
    gen_workspace = {}
    if run_workspace and "files" in run_workspace:
        # We want user's editable content. 
        # Typically run_workspace merges user overlay.
        # So we can just map it.
        for f in run_workspace["files"]:
            gen_workspace[f["path"]] = {"content": f.get("content", "")}
    
    # Or just fallback to payload.
    if not gen_workspace and payload.workspace:
         gen_workspace = {f["path"]: {"content": f.get("content", "")} for f in payload.workspace}
    elif not gen_workspace and payload.code:
         # Legacy single file mode - default to main.py (or main.ts etc)
         # We need to guess the filename or defaults. Python -> main.py
         fname = "main.py" 
         if payload.language == "javascript": fname = "main.js"
         elif payload.language == "typescript": fname = "main.ts"
         
         gen_workspace = {fname: {"content": payload.code}}

    # Helper to handle mixed dict/Pydantic models safely
    def normalize_obj(x):
        if hasattr(x, "model_dump"):
            return x.model_dump()
        return x

    q_fixes = generate_quick_fixes(
        language=payload.language or "python",
        failure_summary=failure_summary,
        diagnostics=diagnostics_data, 
        objective_results=[normalize_obj(r) for r in (objective_results or [])],
        workspace_snapshot=gen_workspace,
        hidden_tests_reveal=True # /run is visible
    )
    attempt.quick_fixes_json = [f.model_dump() for f in q_fixes]

    if passed:
        from arcade_app.services.debrief_generator import generate_debrief
        # ... existing ...
        
        debrief_data = await generate_debrief(db, quest, attempt, prog)
        attempt.debrief_json = debrief_data
    
    # Phase 8.x PR 4: Extract LLM metadata if present
    # Priority: quick_fixes > debrief (quick fixes are closer to error context)
    if attempt.quick_fixes_json and isinstance(attempt.quick_fixes_json, list) and len(attempt.quick_fixes_json) > 0:
        first_fix = attempt.quick_fixes_json[0]
        if isinstance(first_fix, dict) and "meta" in first_fix:
            attempt.model_id = first_fix["meta"].get("model_id")
            attempt.prompt_version = first_fix["meta"].get("prompt_version")
    elif attempt.debrief_json and isinstance(attempt.debrief_json, dict) and "meta" in attempt.debrief_json:
        attempt.model_id = attempt.debrief_json["meta"].get("model_id")
        attempt.prompt_version = attempt.debrief_json["meta"].get("prompt_version")
        
    db.add(attempt)
    db.add(prog) # Ensure prog update is staged
    
    # Phase 8.x PR 3: Handle race conditions on idempotency_key
    try:
        await db.commit()
        await db.refresh(attempt)
    except IntegrityError:
        # Race condition: another request with same key won
        await db.rollback()
        existing = await get_existing_attempt_by_idempotency(
            db, user_id, quest_id, is_submit=False, idempotency_key=payload.idempotency_key
        )
        if existing:
            # Return the other request's result
            prog = await _get_or_create_progress(db, user_id, quest_id)
            return {
                "passed": existing.passed,
                "objective_results": existing.objective_results,
                "stdout": existing.stdout,
                "stderr": existing.stderr,
                "ready_to_submit": existing.passed and not existing.meta.get("timed_out", False),
                "attempt_id": str(existing.id),
                "run_number": existing.meta.get("seq", prog.runs_count),
                "duration_ms": existing.duration_ms,
                "exit_code": existing.meta.get("exit_code", 0),
                "timed_out": existing.meta.get("timed_out", False),
                "coach": existing.meta.get("coach"),
                "debrief": existing.debrief_json if existing.debrief_json else None,
                "diagnostics": existing.diagnostics_json if existing.diagnostics_json else [],
                "quick_fixes": existing.quick_fixes_json if existing.quick_fixes_json else []
            }
        # Unexpected: integrity error but no existing record
        raise

    return {
        "passed": passed,
        "objective_results": objective_results,
        "stdout": stdout,
        "stderr": stderr,
        "ready_to_submit": passed and not timed_out,
        "attempt_id": str(attempt.id),
        "run_number": prog.runs_count,
        "duration_ms": duration_ms,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "coach": coach_data,
        "debrief": debrief_data,
        "diagnostics": diagnostics_data,
        "quick_fixes": q_fixes
    }

@router.get("/{quest_id}/attempts", response_model=list[dict])
async def list_attempts(
    quest_id: str,
    limit: int = 25,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_user_id),
):
    """
    Returns recent attempts for the history rail.
    """
    query = (
        select(QuestAttempt)
        .where(
            QuestAttempt.user_id == user_id,
            QuestAttempt.quest_id == quest_id
        )
        .order_by(desc(QuestAttempt.created_at))
        .limit(limit)
    )
    result = await db.execute(query)
    rows = result.scalars().all()
    
    # Map to simplified model
    return [
        {
            "id": str(r.id),
            "created_at": r.created_at,
            "run_number": r.meta.get("seq", 0),
            "passed": r.passed,
            "is_submit": r.is_submit,
            "duration_ms": r.duration_ms,
            "timed_out": r.meta.get("timed_out", False),
            "exit_code": r.meta.get("exit_code", 0)
        }
        for r in rows
    ]

@router.get("/{quest_id}/attempts/{attempt_id}", response_model=dict)
async def get_attempt_detail(
    quest_id: str,
    attempt_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_user_id),
):
    """
    Returns full artifact for replay.
    """
    query = select(QuestAttempt).where(
        QuestAttempt.id == attempt_id, # UUID cast handled by driver usually
        QuestAttempt.user_id == user_id
    )
    result = await db.execute(query)
    row = result.scalar_one_or_none()
    
    if not row:
        raise HTTPException(404, "Attempt not found")
        
    return {
        "id": str(row.id),
        "code": row.code,
        "stdout": row.stdout,
        "stderr": row.stderr,
        "objective_results": row.objective_results,
        "run_number": row.meta.get("seq", 0),
        "passed": row.passed,
        "duration_ms": row.duration_ms,
        "timed_out": row.meta.get("timed_out", False),
        "is_submit": row.is_submit,
        "created_at": row.created_at
    }

@router.post("/{quest_id}/submit", response_model=dict)
async def submit_quest(
    quest_id: str,
    payload: RunRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_user_id),
):
    # Phase 8.x PR 3: Check for existing submit with same idempotency key
    existing = await get_existing_attempt_by_idempotency(
        db, user_id, quest_id, is_submit=True, idempotency_key=payload.idempotency_key
    )
    if existing:
        # Return existing result
        return {
            "ok": True,
            "quest_id": quest_id,
            "xp_awarded": existing.meta.get("xp", 0),
            "mastery_awarded": 0,
            "objective_results": existing.objective_results,
            "status": "completed",
        }
    
    objective_results = validate_first_sparks_python(payload.code)
    passed = all(o.get("ok") for o in objective_results if o["id"] != "syntax")
    if not passed:
        return {"ok": False, "reason": "Objectives not met", "objective_results": objective_results}

    # award XP (simple for now)
    xp_awarded = 50
    mastery_awarded = 0
    
    # Phase 8.x PR 4: Compute workspace hash + execution context for submit
    from arcade_app.services.workspace_hash import hash_workspace_snapshot, build_execution_context
    
    # For submit, workspace is typically from payload
    workspace_for_hash = None
    if payload.workspace:
        workspace_for_hash = {
            "entrypoint": getattr(payload, "entrypoint", None) or "main.py",
            "files": payload.workspace
        }
    
    workspace_hash = hash_workspace_snapshot(workspace_for_hash)
    execution_context = build_execution_context(
        language=payload.language or "python",
        mode="submit",
        duration_ms=0,  # Submit doesn't execute
        exit_code=0,
        stdout=None,
        stderr=None,
        timed_out=False
    )

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
        idempotency_key=payload.idempotency_key,  # Phase 8.x PR 3
        workspace_hash=workspace_hash,  # Phase 8.x PR 4
        execution_context_json=execution_context,  # Phase 8.x PR 4
    )
    db.add(attempt)

    prog = await _get_or_create_progress(db, user_id, quest_id)
    prog.attempts_count += 1
    prog.status = "completed"
    prog.completed_at = datetime.utcnow()
    prog.last_xp = xp_awarded
    prog.best_xp = max(prog.best_xp, xp_awarded)

    # Phase 8.x PR 3: Handle race conditions
    try:
        await db.commit()
    except IntegrityError:
        # Race condition: another request with same key won
        await db.rollback()
        existing = await get_existing_attempt_by_idempotency(
            db, user_id, quest_id, is_submit=True, idempotency_key=payload.idempotency_key
        )
        if existing:
            return {
                "ok": True,
                "quest_id": quest_id,
                "xp_awarded": existing.meta.get("xp", 0),
                "mastery_awarded": 0,
                "objective_results": existing.objective_results,
                "status": "completed",
            }
        raise

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

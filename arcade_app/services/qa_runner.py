"""
QA Runner Service - Execute on-demand quest validation runs.
Reuses existing code_runner and quest_validate infrastructure.
"""
import os
import uuid
import time
import asyncio
from datetime import datetime
from typing import Dict, Optional
import copy

from sqlmodel import select
from arcade_app.models import QaRun, QuestDefinition
from arcade_app.database import get_session
from arcade_app.services.code_runner import run_code
from arcade_app.services.quest_validate import validate_quest_attempt

# Timeout configuration (configurable via env var)
TIMEOUT_SECONDS = int(os.getenv("QA_TIMEOUT_SECONDS", "60"))


async def execute_qa_run(quest_slug: str, variant: str) -> str:
    """
    Execute a QA run for a quest (starter/solution/integrity).
    Returns the run_id.
    
    Args:
        quest_slug: Quest slug to test
        variant: "starter" | "solution" | "integrity"
    """
    run_id = f"qarun_{uuid.uuid4().hex[:12]}"
    
    async for session in get_session():
        # Fetch quest definition
        quest_result = await session.exec(
            select(QuestDefinition).where(QuestDefinition.slug == quest_slug)
        )
        quest = quest_result.first()
        
        if not quest:
            # Create failed run record
            failed_run = QaRun(
                id=run_id,
                quest_slug=quest_slug,
                variant=variant,
                status="failed",
                result_json={"error": f"Quest '{quest_slug}' not found"}
            )
            session.add(failed_run)
            await session.commit()
            return run_id
        
        # Create run record (queued)
        qa_run = QaRun(
            id=run_id,
            quest_slug=quest_slug,
            variant=variant,
            status="queued",
            engine_version="phase-8.0"
        )
        session.add(qa_run)
        await session.commit()
    
    # Execute in background (simplified - use BackgroundTasks in route)
    # For now, we'll do inline execution
    await _execute_run_logic(run_id, quest, variant)
    
    return run_id


async def _execute_run_logic(run_id: str, quest: QuestDefinition, variant: str):
    """Internal logic to execute the run and update the record."""
    from arcade_app.services.qa_limits import qa_limiter
    
    start_time = time.time()
    
    try:
        async for session in get_session():
            # Update to running
            run_result = await session.exec(select(QaRun).where(QaRun.id == run_id))
            qa_run = run_result.first()
            if not qa_run:
                return
            
            qa_run.status = "running"
            await session.commit()
        
        try:
            # Execute with timeout enforcement
            result = await asyncio.wait_for(
                _run_variant(quest, variant),
                timeout=TIMEOUT_SECONDS
            )
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Update run record with results
            async for session in get_session():
                run_result = await session.exec(select(QaRun).where(QaRun.id == run_id))
                qa_run = run_result.first()
                if qa_run:
                    qa_run.status = "finished"
                    qa_run.duration_ms = duration_ms
                    qa_run.result_json = result
                    qa_run.logs_sanitized = result.get("stdout", "")[:5000]  # Limit size
                    qa_run.diagnostics_json = result.get("diagnostics", {})
                    qa_run.test_summary_json = result.get("test_summary", {})
                    await session.commit()
        
        except asyncio.TimeoutError:
            # Handle timeout
            duration_ms = TIMEOUT_SECONDS * 1000
            async for session in get_session():
                run_result = await session.exec(select(QaRun).where(QaRun.id == run_id))
                qa_run = run_result.first()
                if qa_run:
                    qa_run.status = "failed"
                    qa_run.duration_ms = duration_ms
                    qa_run.result_json = {
                        "passed": False,
                        "error": "timeout",
                        "issues": [f"Test execution exceeded {TIMEOUT_SECONDS}s timeout"]
                    }
                    qa_run.logs_sanitized = f"[TIMEOUT] Execution exceeded {TIMEOUT_SECONDS}s limit"
                    await session.commit()
        
        except Exception as e:
            # Mark as failed
            async for session in get_session():
                run_result = await session.exec(select(QaRun).where(QaRun.id == run_id))
                qa_run = run_result.first()
                if qa_run:
                    qa_run.status = "failed"
                    qa_run.result_json = {"passed": False, "error": str(e)}
                    await session.commit()
    finally:
        # Always unregister run from limiter, even on error
        await qa_limiter.unregister_run(run_id)


async def _run_variant(quest: QuestDefinition, variant: str) -> Dict:
    """Execute variant logic (extracted for timeout wrapper)."""
    if variant == "integrity":
        return await _run_integrity_check(quest)
    elif variant == "solution":
        return await _run_solution(quest)
    elif variant == "starter":
        return await _run_starter(quest)
    else:
        return {"error": f"Unknown variant: {variant}"}


async def _run_starter(quest: QuestDefinition) -> Dict:
    """Run starter code and validate."""
    workspace = quest.workspace_json or {}
    mode = quest.grading_json.get("mode", "run")
    timeout = quest.runtime_rules_json.get("timeout_ms", 5000)
    
    # Mock quest object for validate_quest_attempt
    class MockQuest:
        def __init__(self, q):
            self.objectives_json = q.objectives_json
            self.grading_json = q.grading_json
    
    try:
        exec_result = run_code(
            quest.language or "python",
            quest.starter_code or "",
            timeout_ms=timeout,
            workspace=workspace,
            mode=mode,
            quest_slug=quest.slug
        )
        
        validation_results = validate_quest_attempt(
            code=quest.starter_code or "",
            stdout=exec_result.stdout,
            stderr=exec_result.stderr,
            exit_code=exec_result.exit_code or 0,
            timed_out=exec_result.timed_out,
            quest_def=MockQuest(quest)
        )
        
        passed = all(r["ok"] for r in validation_results) if validation_results else False
        
        return {
            "passed": passed,
            "stdout": exec_result.stdout,
            "stderr": exec_result.stderr,
            "exit_code": exec_result.exit_code,
            "objective_results": validation_results
        }
    except Exception as e:
        return {
            "passed": False,
            "error": str(e),
            "stdout": "",
            "stderr": str(e)
        }


async def _run_solution(quest: QuestDefinition) -> Dict:
    """Run solution code and validate."""
    # Solution code should be in smoke config or workspace solution files
    smoke_config = quest.grading_json.get("smoke", {})  # Might be nested
    solution_code = smoke_config.get("solution_code")
    solution_files = smoke_config.get("solution_workspace_files", [])
    
    if not solution_code and not solution_files:
        return {
            "passed": False,
            "error": "No solution code configured for this quest"
        }
    
    # Build solution workspace
    workspace = copy.deepcopy(quest.workspace_json or {})
    if solution_files:
        if "files" not in workspace:
            workspace["files"] = []
        
        for sf in solution_files:
            # Update or add solution file
            found = False
            for f in workspace["files"]:
                if f["path"] == sf["path"]:
                    f["content"] = sf["content"]
                    found = True
                    break
            if not found:
                workspace["files"].append(sf)
    
    mode = quest.grading_json.get("mode", "run")
    timeout = quest.runtime_rules_json.get("timeout_ms", 5000)
    
    class MockQuest:
        def __init__(self, q):
            self.objectives_json = q.objectives_json
            self.grading_json = q.grading_json
    
    try:
        exec_result = run_code(
            quest.language or "python",
            solution_code or "",
            timeout_ms=timeout,
            workspace=workspace,
            mode=mode,
            quest_slug=quest.slug
        )
        
        validation_results = validate_quest_attempt(
            code=solution_code or "",
            stdout=exec_result.stdout,
            stderr=exec_result.stderr,
            exit_code=exec_result.exit_code or 0,
            timed_out=exec_result.timed_out,
            quest_def=MockQuest(quest)
        )
        
        passed = all(r["ok"] for r in validation_results) if validation_results else False
        
        return {
            "passed": passed,
            "stdout": exec_result.stdout,
            "stderr": exec_result.stderr,
            "exit_code": exec_result.exit_code or 0,
            "objective_results": validation_results
        }
    except Exception as e:
        return {
            "passed": False,
            "error": str(e),
            "stdout": "",
            "stderr": str(e)
        }


async def _run_integrity_check(quest: QuestDefinition) -> Dict:
    """Run both starter (must fail) and solution (must pass)."""
    starter_result = await _run_starter(quest)
    solution_result = await _run_solution(quest)
    
    # Check invariants
    starter_should_fail = not starter_result["passed"]
    solution_should_pass = solution_result["passed"]
    
    integrity_passed = starter_should_fail and solution_should_pass
    
    issues = []
    if not starter_should_fail:
        issues.append("Starter code PASSED but should FAIL")
    if not solution_should_pass:
        issues.append("Solution code FAILED but should PASS")
    
    return {
        "passed": integrity_passed,
        "issues": issues,
        "starter_result": starter_result,
        "solution_result": solution_result
    }

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import Optional, List, Dict
from pathlib import Path
import json

from sqlmodel import select
from arcade_app.models import QaRun, QuestDefinition
from arcade_app.database import get_session
from arcade_app.auth_helper import require_admin
from fastapi import Depends

router = APIRouter(prefix="/api/qa", tags=["qa"])

# Allowlisted artifact files (path traversal prevention)
ALLOWED_ARTIFACTS = {
    "smoke-content-failures.json",
    "smoke-content-failures.md"
}

@router.get("/summary")
async def get_qa_summary(current_user: Dict = Depends(require_admin)):
    """
    Returns global health metrics + per-track breakdown.
    Sources: DB (latest QaRun per quest) + artifact files.
    """
    async for session in get_session():
        # Get all quests
        quests_result = await session.exec(select(QuestDefinition))
        quests = list(quests_result)
        
        # Get latest QA run for each quest
        latest_runs = {}
        for quest in quests:
            runs_result = await session.exec(
                select(QaRun)
                .where(QaRun.quest_slug == quest.slug)
                .order_by(QaRun.created_at.desc())
                .limit(1)
            )
            run = runs_result.first()
            if run:
                latest_runs[quest.slug] = run
        
        # Count healthy vs unhealthy
        healthy_count = 0
        unhealthy_count = 0
        
        for slug, run in latest_runs.items():
            if run.status == "finished" and run.result_json.get("passed", False):
                healthy_count += 1
            else:
                unhealthy_count += 1
        
        # For quests without runs, count as unknown (not included in healthy/unhealthy)
        unknown_count = len(quests) - healthy_count - unhealthy_count
        
        # Group by track
        tracks = {}
        for quest in quests:
            track_key = f"{quest.world_id}/{quest.track_id}"
            if track_key not in tracks:
                tracks[track_key] = {
                    "world_id": quest.world_id,
                    "track_id": quest.track_id,
                    "quests_total": 0,
                    "healthy": 0,
                    "unhealthy": 0,
                    "unknown": 0
                }
            
            tracks[track_key]["quests_total"] += 1
            
            if quest.slug in latest_runs:
                run = latest_runs[quest.slug]
                if run.status == "finished" and run.result_json.get("passed", False):
                    tracks[track_key]["healthy"] += 1
                else:
                    tracks[track_key]["unhealthy"] += 1
            else:
                tracks[track_key]["unknown"] += 1
        
        return {
            "generated_at": "2026-01-31T17:30:00Z",  # TODO: use actual timestamp
            "tracks": list(tracks.values()),
            "global": {
                "quests_total": len(quests),
                "healthy": healthy_count,
                "unhealthy": unhealthy_count,
                "unknown": unknown_count
            }
        }


@router.get("/quests")
async def get_qa_quests(
    world_id: Optional[str] = Query(None),
    track_id: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    current_user: Dict = Depends(require_admin)
):
    """
    Returns list of quests with health status and filters.
    Query params: world_id, track_id, language, status, q (search).
    """
    async for session in get_session():
        query = select(QuestDefinition)
        
        if world_id:
            query = query.where(QuestDefinition.world_id == world_id)
        if track_id:
            query = query.where(QuestDefinition.track_id == track_id)
        if language:
            query = query.where(QuestDefinition.language == language)
        if q:
            query = query.where(
                (QuestDefinition.title.contains(q)) |
                (QuestDefinition.slug.contains(q))
            )
        
        quests_result = await session.exec(query)
        quests = list(quests_result)
        
        # Fetch latest run for each quest
        quest_list = []
        for quest in quests:
            runs_result = await session.exec(
                select(QaRun)
                .where(QaRun.quest_slug == quest.slug)
                .order_by(QaRun.created_at.desc())
                .limit(1)
            )
            latest_run = runs_result.first()
            
            health_status = "unknown"
            if latest_run:
                if latest_run.status == "finished" and latest_run.result_json.get("passed", False):
                    health_status = "healthy"
                elif latest_run.status == "finished":
                    health_status = "unhealthy"
                elif latest_run.status == "running":
                    health_status = "running"
            
            # Apply status filter
            if status and health_status != status:
                continue
            
            quest_list.append({
                "slug": quest.slug,
                "title": quest.title,
                "world_id": quest.world_id,
                "track_id": quest.track_id,
                "language": quest.language,
                "health_status": health_status,
                "last_run_at": latest_run.created_at.isoformat() if latest_run else None,
                "last_run_variant": latest_run.variant if latest_run else None
            })
        
        return {"quests": quest_list}


@router.get("/artifacts/{filename}")
async def get_qa_artifact(filename: str, current_user: Dict = Depends(require_admin)):
    """
    Serves allowlisted artifact files (smoke-content-failures.json/md).
    Strict allowlist to prevent path traversal.
    """
    if filename not in ALLOWED_ARTIFACTS:
        raise HTTPException(status_code=404, detail="Artifact not found or not allowed")
    
    artifact_path = Path("artifacts") / filename
    
    if not artifact_path.exists():
        raise HTTPException(status_code=404, detail="Artifact file not found")
    
    try:
        with open(artifact_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if filename.endswith(".json"):
            return json.loads(content)
        else:
            return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read artifact: {str(e)}")


# Request Models
from pydantic import BaseModel

class QARunRequest(BaseModel):
    quest_id: str
    variant: str = "integrity"


@router.post("/run")
async def create_qa_run(
    request: QARunRequest,
    background_tasks: BackgroundTasks = None,
    current_user: Dict =Depends(require_admin)
):
    """
    Trigger an on-demand QA run for a quest.
    
    Body: { "quest_id": "quest-py-hidden", "variant": "starter|solution|integrity" }
    Returns: { "run_id": "qarun_123", "status": "queued" }
    """
    from arcade_app.services.qa_runner import execute_qa_run
    from arcade_app.services.qa_limits import qa_limiter
    
    user_id = current_user.get("id", "anonymous")
    
    # Check rate limits
    if not await qa_limiter.can_start_run(user_id):
        active_count = await qa_limiter.get_active_count(user_id)
        raise HTTPException(
            status_code=429,
            detail={
                "error": "rate_limit_exceeded",
                "message": "Too many concurrent QA runs. Please wait for existing runs to complete.",
                "limits": {
                    "global": qa_limiter.global_limit,
                    "per_user": qa_limiter.per_user_limit
                },
                "current": {
                    "user_active_runs": active_count
                }
            }
        )
    
    if request.variant not in ["starter", "solution", "integrity"]:
        raise HTTPException(status_code=400, detail="Invalid variant. Must be starter, solution, or integrity")
    
    try:
        run_id = await execute_qa_run(request.quest_id, request.variant)
        # Register run in limiter
        await qa_limiter.register_run(run_id, user_id)
        return {"run_id": run_id, "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create QA run: {str(e)}")


@router.get("/runs/{run_id}")
async def get_qa_run(run_id: str, current_user: Dict = Depends(require_admin)):
    """
    Get the status and results of a QA run.
    Polling endpoint for frontend.
    """
    async for session in get_session():
        run_result = await session.exec(select(QaRun).where(QaRun.id == run_id))
        qa_run = run_result.first()
        
        if not qa_run:
            raise HTTPException(status_code=404, detail="QA run not found")
        
        return {
            "id": qa_run.id,
            "quest_slug": qa_run.quest_slug,
            "variant": qa_run.variant,
            "status": qa_run.status,
            "duration_ms": qa_run.duration_ms,
            "result": qa_run.result_json,
            "logs": qa_run.logs_sanitized,
            "diagnostics": qa_run.diagnostics_json,
            "test_summary": qa_run.test_summary_json,
            "created_at": qa_run.created_at.isoformat()
        }


# ===== BATCH RUN ENDPOINTS (Phase 8.1) =====

class QABatchRunRequest(BaseModel):
    world_id: Optional[str] = None
    track_id: Optional[str] = None
    variant: str = "integrity"


@router.post("/batch/run")
async def create_batch_run(
    request: QABatchRunRequest,
    current_user: Dict = Depends(require_admin)
):
    """
    Trigger batch integrity check for all quests in a track.
    
    Body: { "world_id": "world-python", "track_id": "basics", "variant": "integrity" }
    Returns: { "batch_id": "qabatch_123", "status": "queued", "total_quests": 12 }
    """
    from arcade_app.services.qa_batch_runner import execute_batch_run
    from arcade_app.models import QaBatchRun
    
    if request.variant not in ["starter", "solution", "integrity"]:
        raise HTTPException(status_code=400, detail="Invalid variant")
    
    if not request.world_id and not request.track_id:
        raise HTTPException(status_code=400, detail="Must specify at least world_id or track_id")
    
    user_id = current_user.get("id", "anonymous")
    
    try:
        batch_id = await execute_batch_run(
            world_id=request.world_id,
            track_id=request.track_id,
            variant=request.variant,
            user_id=user_id
        )
        
        # Fetch batch to return details
        async for session in get_session():
            batch_result = await session.exec(
                select(QaBatchRun).where(QaBatchRun.id == batch_id)
            )
            batch = batch_result.first()
            if batch:
                return {
                    "batch_id": batch.id,
                    "status": batch.status,
                    "total_quests": batch.total_quests,
                    "world_id": batch.world_id,
                    "track_id": batch.track_id
                }
            break
        
        raise HTTPException(status_code=500, detail="Batch created but not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create batch: {str(e)}")


@router.get("/batch/runs/{batch_id}")
async def get_batch_run(
    batch_id: str,
    current_user: Dict = Depends(require_admin)
):
    """
    Get batch run status and progress.
    
    Returns: {
        "batch_id": "qabatch_123",
        "status": "running",
        "total_quests": 12,
        "completed_quests": 7,
        "passed_count": 5,
        "failed_count": 2,
        "progress_percent": 58
    }
    """
    from arcade_app.models import QaBatchRun
    
    async for session in get_session():
        batch_result = await session.exec(
            select(QaBatchRun).where(QaBatchRun.id == batch_id)
        )
        batch = batch_result.first()
        
        if not batch:
            raise HTTPException(status_code=404, detail="Batch run not found")
        
        progress_percent = 0
        if batch.total_quests > 0:
            progress_percent = int((batch.completed_quests / batch.total_quests) * 100)
        
        return {
            "batch_id": batch.id,
            "status": batch.status,
            "world_id": batch.world_id,
            "track_id": batch.track_id,
            "variant": batch.variant,
            "total_quests": batch.total_quests,
            "completed_quests": batch.completed_quests,
            "passed_count": batch.passed_count,
            "failed_count": batch.failed_count,
            "progress_percent": progress_percent,
            "duration_ms": batch.duration_ms,
            "created_at": batch.created_at.isoformat() if batch.created_at else None,
            "started_at": batch.started_at.isoformat() if batch.started_at else None,
            "finished_at": batch.finished_at.isoformat() if batch.finished_at else None
        }


@router.get("/batch/runs/{batch_id}/quests")
async def get_batch_quest_results(
    batch_id: str,
    current_user: Dict = Depends(require_admin)
):
    """
    Get individual quest results for a batch run.
    
    Returns: {
        "batch_id": "qabatch_123",
        "quests": [
            {
                "quest_slug": "quest-py-hello",
                "run_id": "qarun_456",
                "status": "finished",
                "passed": true
            },
            ...
        ]
    }
    """
    from arcade_app.models import QaBatchRun
    
    async for session in get_session():
        # Verify batch exists
        batch_result = await session.exec(
            select(QaBatchRun).where(QaBatchRun.id == batch_id)
        )
        batch = batch_result.first()
        if not batch:
            raise HTTPException(status_code=404, detail="Batch run not found")
        
        # Get all runs for this batch
        runs_result = await session.exec(
            select(QaRun).where(QaRun.batch_id == batch_id)
        )
        runs = list(runs_result)
        
        quest_results = []
        for run in runs:
            quest_results.append({
                "quest_slug": run.quest_slug,
                "run_id": run.id,
                "status": run.status,
                "passed": run.result_json.get("passed", False) if run.result_json else False,
                "duration_ms": run.duration_ms,
                "issues": run.result_json.get("issues", []) if run.result_json else []
            })
        
        return {
            "batch_id": batch.id,
            "quests": quest_results
        }

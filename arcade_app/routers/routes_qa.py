from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import Optional, List, Dict
from pathlib import Path
import json

from sqlmodel import select
from arcade_app.models import QaRun, QuestDefinition
from arcade_app.config import get_async_session

router = APIRouter(prefix="/api/qa", tags=["qa"])

# Allowlisted artifact files (path traversal prevention)
ALLOWED_ARTIFACTS = {
    "smoke-content-failures.json",
    "smoke-content-failures.md"
}

@router.get("/summary")
async def get_qa_summary():
    """
    Returns global health metrics + per-track breakdown.
    Sources: DB (latest QaRun per quest) + artifact files.
    """
    async with get_async_session() as session:
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
    q: Optional[str] = Query(None)
):
    """
    Returns list of quests with health status and filters.
    Query params: world_id, track_id, language, status, q (search).
    """
    async with get_async_session() as session:
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
async def get_qa_artifact(filename: str):
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


@router.post("/run")
async def create_qa_run(
    quest_id: str,
    variant: str = "integrity",
    background_tasks: BackgroundTasks = None
):
    """
    Trigger an on-demand QA run for a quest.
    
    Body: { "quest_id": "quest-py-hidden", "variant": "starter|solution|integrity" }
    Returns: { "run_id": "qarun_123", "status": "queued" }
    """
    from arcade_app.services.qa_runner import execute_qa_run
    
    if variant not in ["starter", "solution", "integrity"]:
        raise HTTPException(status_code=400, detail="Invalid variant. Must be starter, solution, or integrity")
    
    try:
        run_id = await execute_qa_run(quest_id, variant)
        return {"run_id": run_id, "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create QA run: {str(e)}")


@router.get("/runs/{run_id}")
async def get_qa_run(run_id: str):
    """
    Get the status and results of a QA run.
    Polling endpoint for frontend.
    """
    async with get_async_session() as session:
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


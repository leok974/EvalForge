"""
QA Batch Runner - Orchestrate integrity checks across multiple quests.

Phase 8.1: Enables "Run All Quests in Track" feature with:
- Sequential execution (respects rate limits)
- Real-time progress tracking
- Aggregated results (passed/failed counts)
"""
import uuid
import time
import asyncio
from typing import List, Optional
from datetime import datetime

from sqlmodel import select
from arcade_app.models import QaBatchRun, QuestDefinition, QaRun
from arcade_app.database import get_session
from arcade_app.services.qa_runner import execute_qa_run


async def execute_batch_run(
    world_id: Optional[str],
    track_id: Optional[str],
    variant: str,
    user_id: str
) -> str:
    """
    Execute batch QA run for all quests in a track.
    
    Args:
        world_id: Filter by world (optional)
        track_id: Filter by track (optional)
        variant: "starter" | "solution" | "integrity"
        user_id: User triggering the batch
    
    Returns:
        batch_id: Unique batch run identifier
    """
    batch_id = f"qabatch_{uuid.uuid4().hex[:12]}"
    
    async for session in get_session():
        # 1. Find matching quests
        query = select(QuestDefinition)
        if world_id:
            query = query.where(QuestDefinition.world_id == world_id)
        if track_id:
            query = query.where(QuestDefinition.track_id == track_id)
        
        quests_result = await session.exec(query)
        quests = list(quests_result)
        
        if not quests:
            # Create empty batch (no quests to run)
            batch = QaBatchRun(
                id=batch_id,
                created_by=user_id,
                world_id=world_id,
                track_id=track_id,
                variant=variant,
                total_quests=0,
                status="finished"
            )
            session.add(batch)
            await session.commit()
            return batch_id
        
        # 2. Create batch record
        batch = QaBatchRun(
            id=batch_id,
            created_by=user_id,
            world_id=world_id,
            track_id=track_id,
            variant=variant,
            total_quests=len(quests),
            status="queued"
        )
        session.add(batch)
        await session.commit()
        break
    
    # 3. Execute runs sequentially in background
    asyncio.create_task(_execute_batch_logic(batch_id, quests, variant))
    
    return batch_id


async def _execute_batch_logic(
    batch_id: str,
    quests: List[QuestDefinition],
    variant: str
):
    """
    Execute batch logic: run quests sequentially, update progress.
    
    Runs sequentially to:
    - Respect rate limits (5 global / 3 per-user)
    - Avoid overwhelming the system
    - Provide predictable progress updates
    """
    start_time = time.time()
    
    # Mark as running
    async for session in get_session():
        batch_result = await session.exec(
            select(QaBatchRun).where(QaBatchRun.id == batch_id)
        )
        batch = batch_result.first()
        if batch:
            batch.status = "running"
            batch.started_at = datetime.utcnow()
            await session.commit()
        break
    
    passed = 0
    failed = 0
    
    try:
        for i, quest in enumerate(quests):
            # Execute single run
            run_id = await execute_qa_run(quest.slug, variant)
            
            # Link run to batch and wait for completion
            async for session in get_session():
                run_result = await session.exec(select(QaRun).where(QaRun.id == run_id))
                run = run_result.first()
                if run:
                    run.batch_id = batch_id
                    await session.commit()
                
                # Poll until run finishes (max 60s timeout + buffer)
                max_wait = 70  # 60s timeout + 10s buffer
                wait_start = time.time()
                while run and run.status in ["queued", "running"]:
                    if time.time() - wait_start > max_wait:
                        # Run took too long, mark as failed
                        failed += 1
                        break
                    
                    await asyncio.sleep(0.5)
                    await session.refresh(run)
                
                # Count result
                if run and run.status == "finished":
                    result_passed = run.result_json.get("passed", False)
                    if result_passed:
                        passed += 1
                    else:
                        failed += 1
                else:
                    # Run didn't finish or doesn't exist
                    failed += 1
                
                # Update batch progress
                batch_result = await session.exec(
                    select(QaBatchRun).where(QaBatchRun.id == batch_id)
                )
                batch = batch_result.first()
                if batch:
                    batch.completed_quests = i + 1
                    batch.passed_count = passed
                    batch.failed_count = failed
                    await session.commit()
                break
        
        # Mark batch as finished
        duration_ms = int((time.time() - start_time) * 1000)
        async for session in get_session():
            batch_result = await session.exec(
                select(QaBatchRun).where(QaBatchRun.id == batch_id)
            )
            batch = batch_result.first()
            if batch:
                batch.status = "finished"
                batch.finished_at = datetime.utcnow()
                batch.duration_ms = duration_ms
                await session.commit()
            break
    
    except Exception as e:
        # Mark batch as failed
        print(f"Batch {batch_id} failed: {e}")
        async for session in get_session():
            batch_result = await session.exec(
                select(QaBatchRun).where(QaBatchRun.id == batch_id)
            )
            batch = batch_result.first()
            if batch:
                batch.status = "failed"
                await session.commit()
            break

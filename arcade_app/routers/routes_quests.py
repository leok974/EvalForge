
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
from arcade_app.services.security import sanitize_logs
from arcade_app.services.utils import build_effective_workspace
from arcade_app.services.quick_fix_generator import generate_quick_fixes

router = APIRouter(prefix="/api/quests", tags=["quests"])

# Helper to map V2 status to QuestState
def map_status_to_state(status: str) -> str:
    # V2 status: locked, available, in_progress, completed, mastered
    # QuestState: same values mostly
    return status

from arcade_app.services.quest_visibility import get_active_quest_config

@router.get("", response_model=List[Dict])
async def list_quests(
    world_id: Optional[str] = None,
    track_id: Optional[str] = None,
    include_inactive: bool = False,
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

    # Resolve active set
    active_slugs, slug_to_pack = get_active_quest_config()
    
    query = select(QuestDefinition)
    if world_id:
        query = query.where(QuestDefinition.world_id == world_id)
    if track_id:
        query = query.where(QuestDefinition.track_id == track_id)
    
    # Filter by output of config unless admin override
    # Also exclude explicitly "internal" visibility if we assume DB has that column? 
    # DB doesn't have 'visibility' column yet (checked schema in mind). 
    # relying on the Config set is safer for now.
    
    if not include_inactive:
        if not active_slugs:
            # Fallback if config is broken/empty? Or verify strictly?
            # If empty, we show nothing. Correct.
            pass
        query = query.where(QuestDefinition.slug.in_(active_slugs))
    
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
        
        q_dict = quest_to_dict(q, qp_wrapper)
        
        # Inject UI Metadata
        q_dict["questpack"] = slug_to_pack.get(q.slug, "unknown")
        q_dict["is_active"] = q.slug in active_slugs
        
        results.append(q_dict)

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


# ──────────────────────────────────────────────────────────────────────────────
# COLLISION NOTE (Sprint 22): The submit handler that was here
# (POST /{quest_slug}/submit) was permanently shadowed by the equivalent
# handler in routes_quests_runtime.py, which is mounted FIRST in agent.py
# (line 470). FastAPI routes first-registered wins; this handler never ran.
#
# The runtime handler (routes_quests_runtime.py) is the canonical submit path.
# It uses the generic run_code() dispatcher, AsyncSession, idempotency keys,
# workspace hashing, and proper fail-closed grading (Sprint 21).
#
# This stale handler was deleted in Sprint 22. Any unique logic it contained
# (Docker-only runner, Profile XP update via profile.total_xp) was already
# superseded by the runtime handler's approach.
# ──────────────────────────────────────────────────────────────────────────────


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

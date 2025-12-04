
from typing import List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from pydantic import BaseModel

from arcade_app.database import get_session
from arcade_app.auth_helper import get_current_user
from arcade_app.models import QuestDefinition, QuestProgress, QuestState, Profile
from arcade_app.quest_helper import quest_to_dict, get_or_create_progress, record_quest_submission

router = APIRouter(prefix="/api/quests", tags=["quests"])

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
    
    # Fetch progress
    progress_stmt = select(QuestProgress).where(
        QuestProgress.user_id == user_id,
        QuestProgress.quest_id.in_([q.id for q in quests])
    )
    result = await session.exec(progress_stmt)
    progress_entries = result.all()
    progress_map = {p.quest_id: p for p in progress_entries}
    
    return [quest_to_dict(q, progress_map.get(q.id)) for q in quests]


@router.post("/{quest_slug}/accept", response_model=Dict)
async def accept_quest(
    quest_slug: str,
    session: Session = Depends(get_session),
    user_data: Dict = Depends(get_current_user),
):
    if not user_data:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    user_id = user_data["id"]
    result = await session.exec(select(Profile).where(Profile.user_id == user_id))
    profile = result.first()
    if not profile:
         raise HTTPException(status_code=404, detail="Profile not found")
    
    result = await session.exec(select(QuestDefinition).where(QuestDefinition.slug == quest_slug))
    quest = result.first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
        
    qp = await get_or_create_progress(session, profile, quest)
    
    if qp.state == QuestState.LOCKED:
        # TODO: Check prerequisites here
        qp.state = QuestState.AVAILABLE
        
    if qp.state in (QuestState.AVAILABLE, QuestState.LOCKED):
        qp.state = QuestState.IN_PROGRESS
        session.add(qp)
        await session.commit()
        await session.refresh(qp)
        
    return quest_to_dict(quest, qp)


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
    if not user_data:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    user_id = user_data["id"]
    result = await session.exec(select(Profile).where(Profile.user_id == user_id))
    profile = result.first()
    if not profile:
         raise HTTPException(status_code=404, detail="Profile not found")

    result = await session.exec(select(QuestDefinition).where(QuestDefinition.slug == quest_slug))
    quest = result.first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")

    from arcade_app.grading_helper import grade_quest_submission
    from arcade_app.quest_helper import apply_quest_unlocks

    score, passed = await grade_quest_submission(
        user=profile,
        quest=quest,
        code=payload.code,
        language=payload.language,
    )

    # Before updating, capture previous state for XP logic
    result = await session.exec(
        select(QuestProgress).where(
            QuestProgress.user_id == user_id,
            QuestProgress.quest_id == quest.id
        )
    )
    existing_qp = result.first()
    
    prev_state = existing_qp.state if existing_qp else None
        
    qp = await record_quest_submission(session, profile, quest, score=score, passed=passed)
    
    # Simple XP logic:
    # - first time reaching COMPLETED => base_xp_reward
    # - first time reaching MASTERED => mastery_xp_bonus
    xp_awarded = 0
    if passed:
        if prev_state not in (QuestState.COMPLETED, QuestState.MASTERED) and qp.state in (
            QuestState.COMPLETED,
            QuestState.MASTERED,
        ):
            xp_awarded += quest.base_xp_reward
        if prev_state != QuestState.MASTERED and qp.state == QuestState.MASTERED:
            xp_awarded += quest.mastery_xp_bonus or 0
 
        # Hook into Profile XP
        if xp_awarded > 0:
            profile.total_xp = (profile.total_xp or 0) + xp_awarded
            session.add(profile)
    
    # Apply boss/layout unlocks
    unlock_events = apply_quest_unlocks(
        session=session,
        user=profile,
        quest=quest,
        prev_state=prev_state,
        new_state=qp.state,
    )

    await session.commit()
    await session.refresh(qp)
    await session.refresh(profile)
    
    return {
        "quest": quest_to_dict(quest, qp),
        "score": score,
        "passed": passed,
        "xp_awarded": xp_awarded,
        "unlock_events": unlock_events,
        "profile": {
            "xp": profile.total_xp,
            "flags": profile.flags,
        },
    }

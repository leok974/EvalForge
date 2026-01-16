from fastapi import APIRouter, Depends, Request, HTTPException
from sqlmodel import select
from ..database import get_session, AsyncSession
from ..auth_helper import get_current_user
from ..models import Profile
from ..practice.service_senior import get_senior_progress, SeniorProgressResponse
from ..agent import WORLDS # Using global dict for metadata
from ..practice.starter import ensure_starter_unlocked
from ..models import User

router = APIRouter(prefix="/api/profile", tags=["profile"])

@router.get("/senior_progress", response_model=SeniorProgressResponse)
async def senior_progress(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    user_dict = await get_current_user(request)
    if not user_dict:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    stmt = select(Profile).where(Profile.user_id == user_dict["id"])
    profile = (await session.exec(stmt)).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    worlds_list = list(WORLDS.values())

    return await get_senior_progress(session, profile, worlds_list)

    return await get_senior_progress(session, profile, worlds_list)

@router.get("/me")
async def get_my_profile(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    user_dict = await get_current_user(request)
    if not user_dict:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_id = user_dict["id"]
    
    # 1. Fetch Profile
    stmt = select(Profile).where(Profile.user_id == user_id)
    profile = (await session.exec(stmt)).first()
    
    # 2. Lazy Create if needed
    if not profile:
        # Ensure user exists first
        user = await session.get(User, user_id)
        if not user:
            user = User(id=user_id, name=f"{user_id} (Dev)")
            session.add(user)
            # Flush to ensure user exists for FK
            await session.flush()
            
        profile = Profile(
            user_id=user_id,
            total_xp=0,
            global_level=1,
            world_progress={}
        )
        session.add(profile)
        await session.commit()
        await session.refresh(profile)

    # 3. Ensure Starter Quest Unlocked
    await ensure_starter_unlocked(session, profile)
    
    # 4. Return Profile (minimal or full, leveraging SQLModel)
    return profile

@router.get("/progress")
async def get_progress(
    request: Request,
    db: AsyncSession = Depends(get_session),
):
    user_dict = await get_current_user(request)
    if not user_dict:
        # Dev fallback if needed, or consistent 401
        # For now, mimic get_my_profile behavior
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    user_id = user_dict["id"]
    from arcade_app.progress_models import QuestProgressV2
    
    # Query progress
    rows = (await db.execute(select(QuestProgressV2).where(QuestProgressV2.user_id == user_id))).scalars().all()
    
    return {
        "user_id": user_id,
        "quests": [
            {
                "quest_id": r.quest_id,
                "status": r.status,
                "best_xp": r.best_xp,
                "last_xp": r.last_xp,
                "attempts_count": r.attempts_count,
                "runs_count": r.runs_count,
                "hint_tier_unlocked": r.hint_tier_unlocked,
                "completed_at": r.completed_at,
            } for r in rows
        ]
    }

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

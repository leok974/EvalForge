from fastapi import APIRouter, Depends, Request, HTTPException
from sqlmodel import select
from ..database import get_session, AsyncSession
from ..auth_helper import get_current_user
from ..models import Profile
from ..practice.service_senior import get_senior_progress, SeniorProgressResponse
from ..agent import WORLDS # Using global dict for metadata

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

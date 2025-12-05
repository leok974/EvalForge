# arcade_app/routers/routes_practice_rounds.py
from datetime import date

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from arcade_app.database import get_session
from arcade_app.models import Profile, User
from arcade_app.auth_helper import get_current_user
from arcade_app.practice_gauntlet import (
    DailyPracticePlan,
    get_daily_practice_plan_for_profile_foundry_applylens,
)

router = APIRouter(
    prefix="/api/practice_rounds",
    tags=["practice-rounds"],
)


@router.get("/today", response_model=DailyPracticePlan)
async def get_today_practice_round(
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
) -> DailyPracticePlan:
    """
    Return today's Practice Gauntlet for the current player.

    Phase 0: scoped to Foundry (world-python) and ApplyLens.
    
    Note: This is a dev/gameplay route, not admin-only.
    In mock mode (EVALFORGE_AUTH_MODE=mock), it will work without real auth.
    """
    # Get user
    user_id = current_user.get("id") or current_user.get("email") or "dev-user"
    
    # Try to get existing user - properly await async session
    user_stmt = select(User).where(User.id == user_id)
    result = await session.execute(user_stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        # Ensure default avatar exists BEFORE creating user (prevents FK violation)
        from arcade_app.auth_helper import ensure_default_avatar
        await ensure_default_avatar(session)
        
        # Create dev user for testing
        user = User(
            id=user_id,
            name=current_user.get("name", "Dev User"),
            avatar_url=current_user.get("avatar_url", ""),
            # current_avatar_id will use model default ("default_user") which now exists
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    
    # Get or create profile - properly await async session
    profile_stmt = select(Profile).where(Profile.user_id == user.id)
    result = await session.execute(profile_stmt)
    profile = result.scalar_one_or_none()
    
    if not profile:
        # Create profile
        profile = Profile(
            user_id=user.id,
            display_name=user.name,
            current_level=1,
            total_xp=0,
        )
        session.add(profile)
        await session.commit()
        await session.refresh(profile)
    
    today = date.today()
    return await get_daily_practice_plan_for_profile_foundry_applylens(
        db=session,
        profile=profile,
        today=today,
    )

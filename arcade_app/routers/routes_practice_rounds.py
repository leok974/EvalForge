# arcade_app/routers/routes_practice_rounds.py
from datetime import date

from fastapi import APIRouter, Depends
from sqlmodel import Session

from arcade_app.database import get_session
from arcade_app.models import Profile
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
    # Get or create profile from user
    # For Phase 0, we'll use a simple approach
    from sqlmodel import select
    from arcade_app.models import Profile, User
    
    # Get user
    user_id = current_user.get("id") or current_user.get("email") or "dev-user"
    
    # Try to get existing user
    user_stmt = select(User).where(User.id == user_id)
    user = session.exec(user_stmt).first()
    
    if not user:
        # Create dev user for testing
        user = User(
            id=user_id,
            name=current_user.get("name", "Dev User"),
            avatar_url=current_user.get("avatar_url", ""),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    
    # Get or create profile
    profile_stmt = select(Profile).where(Profile.user_id == user.id)
    profile = session.exec(profile_stmt).first()
    
    if not profile:
        # Create profile
        profile = Profile(
            user_id=user.id,
            display_name=user.name,
            current_level=1,
            total_xp=0,
        )
        session.add(profile)
        session.commit()
        session.refresh(profile)
    
    today = date.today()
    return get_daily_practice_plan_for_profile_foundry_applylens(
        db=session,
        profile=profile,
        today=today,
    )

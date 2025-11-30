import math
from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import User, Profile

async def get_profile(user_id: str) -> dict:
    """
    Retrieves profile from Postgres. Creates User/Profile if missing.
    """
    async for session in get_session():
        # 1. Try to fetch profile
        statement = select(Profile).where(Profile.user_id == user_id)
        result = await session.execute(statement)
        profile = result.scalar_one_or_none()

        # 2. Lazy Init if missing
        if not profile:
            # Check if user exists, else create
            user = await session.get(User, user_id)
            if not user:
                user = User(id=user_id, name=f"{user_id} (Dev)")
                session.add(user)
            
            profile = Profile(
                user_id=user_id, 
                total_xp=0, 
                global_level=1, 
                world_progress={}
            )
            session.add(profile)
            await session.commit()
            await session.refresh(profile)
        
        # 3. Return Dict (matching old API contract)
        return {
            "total_xp": profile.total_xp,
            "level": profile.global_level,
            "world_progress": profile.world_progress or {},
            "recent_badges": [] 
        }

async def add_xp(user_id: str, world_id: str, amount: int) -> dict:
    """
    Transactional XP update.
    """
    async for session in get_session():
        # Fetch
        statement = select(Profile).where(Profile.user_id == user_id)
        result = await session.execute(statement)
        profile = result.scalar_one_or_none()
        
        # Guard clause: Ensure profile exists
        if not profile:
            await get_profile(user_id) # Recursive init
            # Re-fetch
            result = await session.execute(statement)
            profile = result.scalar_one_or_none()

        # Update Logic
        profile.total_xp += amount
        old_global_level = profile.global_level
        profile.global_level = math.floor(profile.total_xp / 1000) + 1

        # Handle JSON field mutation
        # SQLModel/SQLAlchemy requires re-assigning JSON dicts to track changes
        wp = dict(profile.world_progress) if profile.world_progress else {}
        w_stats = wp.setdefault(world_id, {"xp": 0, "level": 1})
        w_stats["xp"] += amount
        old_world_level = w_stats["level"]
        w_stats["level"] = math.floor(w_stats["xp"] / 100) + 1
        
        profile.world_progress = wp 
        
        session.add(profile)
        await session.commit()
        
        return {
            "xp_gained": amount,
            "world_id": world_id,
            "new_world_level": w_stats["level"],
            "world_level_up": w_stats["level"] > old_world_level,
            "new_global_level": profile.global_level,
            "global_level_up": profile.global_level > old_global_level
        }

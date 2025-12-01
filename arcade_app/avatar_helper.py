from typing import List, Dict
from sqlmodel import select
from sqlalchemy import update
from arcade_app.database import get_session
from arcade_app.models import User, AvatarDefinition
from arcade_app.profile_helper import get_profile

async def list_avatars(user_id: str) -> List[Dict]:
    """Lists all avatars with lock status for the user."""
    profile = await get_profile(user_id)
    user_level = profile["level"]
    
    async for session in get_session():
        # Get current equipped
        user = await session.get(User, user_id)
        current_id = user.current_avatar_id if user else "default_user"

        statement = select(AvatarDefinition).where(AvatarDefinition.is_active == True)
        results = await session.execute(statement)
        avatars = results.scalars().all()
        
        output = []
        for av in avatars:
            is_locked = user_level < av.required_level
            output.append({
                **av.dict(),
                "is_locked": is_locked,
                "is_equipped": (av.id == current_id)
            })
        return output

async def equip_avatar(user_id: str, avatar_id: str) -> Dict:
    async for session in get_session():
        # We need to fetch avatar to check requirements
        avatar = await session.get(AvatarDefinition, avatar_id)
        
        if not avatar:
             return {"error": "Avatar not found"}

        # Check Level Gate
        profile = await get_profile(user_id)
        if profile["level"] < avatar.required_level:
             return {"error": f"Level {avatar.required_level} required."}

        # Use explicit update to avoid ORM session issues
        print(f"DEBUG: Executing update for user {user_id} to avatar {avatar.id}")
        stmt = update(User).where(User.id == user_id).values(current_avatar_id=avatar.id)
        result = await session.execute(stmt)
        print(f"DEBUG: Update rowcount: {result.rowcount}")
        
        # Debug: List all users
        users = (await session.execute(select(User))).scalars().all()
        print(f"DEBUG: All users: {[(u.id, u.current_avatar_id) for u in users]}")

        await session.commit()
        print("DEBUG: Update executed and committed")
        
        return {"status": "ok", "equipped": avatar.id}

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from typing import List

from arcade_app.database import get_session
from arcade_app.models import AvatarDefinition, User, Profile
from arcade_app.auth_helper import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/api/avatars", tags=["avatars"])

class EquipAvatarRequest(BaseModel):
    avatar_id: str

from typing import Dict

async def _get_user_level(user: Dict, session) -> int:
    # If you store level on Profile:
    result = await session.execute(
        select(Profile).where(Profile.user_id == user["id"])
    )
    profile = result.scalars().first()
    
    if profile and getattr(profile, "global_level", None) is not None:
        return profile.global_level
    # fallback
    return 1


@router.get("", name="list_avatars")
async def list_avatars(
    current_user: Dict = Depends(get_current_user),
    session=Depends(get_session),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    async with session as s:
        result = await s.execute(
            select(AvatarDefinition).where(AvatarDefinition.is_active == True)
        )
        avatars: List[AvatarDefinition] = result.scalars().all()

        user_level = await _get_user_level(current_user, s)

        items = []
        for av in avatars:
            is_locked = user_level < av.required_level
            items.append(
                {
                    "id": av.id,
                    "name": av.name,
                    "description": av.description,
                    "required_level": av.required_level,
                    "rarity": av.rarity,
                    "visual_type": av.visual_type,
                    "visual_data": av.visual_data,
                    "is_locked": is_locked,
                    "is_equipped": (current_user.get("current_avatar_id") == av.id),
                }
            )

        return {"avatars": items}

@router.post("/equip", name="equip_avatar")
async def equip_avatar(
    payload: EquipAvatarRequest,
    current_user: Dict = Depends(get_current_user),
    session=Depends(get_session),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    async with session as s:
        avatar = await s.get(AvatarDefinition, payload.avatar_id)
        if not avatar or not avatar.is_active:
            raise HTTPException(status_code=404, detail="Avatar not found")

        user_level = await _get_user_level(current_user, s)
        if user_level < avatar.required_level:
            raise HTTPException(
                status_code=403,
                detail=f"Avatar requires level {avatar.required_level}",
            )

        # Update User object in DB
        # We need to fetch the User object first since we only have a Dict
        user_obj = await s.get(User, current_user["id"])
        if not user_obj:
             raise HTTPException(status_code=404, detail="User not found")

        user_obj.current_avatar_id = avatar.id
        s.add(user_obj)
        await s.commit()
        await s.refresh(user_obj)

        return {
            "status": "ok",
            "current_avatar_id": user_obj.current_avatar_id,
        }

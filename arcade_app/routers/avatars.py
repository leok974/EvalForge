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

def _get_user_level(user: User, session) -> int:
    # If you store level on Profile:
    profile = session.exec(
        select(Profile).where(Profile.user_id == user.id)
    ).first()
    if profile and getattr(profile, "global_level", None) is not None:
        return profile.global_level
    # fallback
    return 1


@router.get("", name="list_avatars")
async def list_avatars(
    current_user: User = Depends(get_current_user),
    session=Depends(get_session),
):
    async with session as s:
        avatars: List[AvatarDefinition] = (
            await s.exec(
                select(AvatarDefinition).where(AvatarDefinition.is_active == True)
            )
        ).all()

        user_level = _get_user_level(current_user, s)

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
                    "is_equipped": (current_user.current_avatar_id == av.id),
                }
            )

        return {"avatars": items}

@router.post("/equip", name="equip_avatar")
async def equip_avatar(
    payload: EquipAvatarRequest,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session),
):
    async with session as s:
        avatar = await s.get(AvatarDefinition, payload.avatar_id)
        if not avatar or not avatar.is_active:
            raise HTTPException(status_code=404, detail="Avatar not found")

        user_level = _get_user_level(current_user, s)
        if user_level < avatar.required_level:
            raise HTTPException(
                status_code=403,
                detail=f"Avatar requires level {avatar.required_level}",
            )

        current_user.current_avatar_id = avatar.id
        s.add(current_user)
        await s.commit()
        await s.refresh(current_user)

        return {
            "status": "ok",
            "current_avatar_id": current_user.current_avatar_id,
        }

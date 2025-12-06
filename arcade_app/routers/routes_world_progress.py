from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from arcade_app.database import get_session
from arcade_app.auth_helper import get_current_user
from arcade_app.progress_helper import compute_track_progress_for_user

router = APIRouter(prefix="/api/worlds", tags=["world-progress"])

class TrackProgressDTO(BaseModel):
    world_slug: str
    track_slug: str
    label: str
    progress: float  # 0–100
    total_quests: int
    completed_quests: int

class WorldProgressResponse(BaseModel):
    tracks: List[TrackProgressDTO]

@router.get("/progress", response_model=WorldProgressResponse)
async def get_world_progress(
    current_user: Dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> WorldProgressResponse:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    rows = await compute_track_progress_for_user(db, current_user["id"])

    return WorldProgressResponse(
        tracks=[
            TrackProgressDTO(**row) for row in rows
        ]
    )

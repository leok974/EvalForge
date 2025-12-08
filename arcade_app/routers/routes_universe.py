from typing import List, Dict, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import select, Session

from arcade_app.database import get_session
from arcade_app.models import TrackDefinition, BossDefinition

router = APIRouter(prefix="/api/universe", tags=["universe"])

class TrackDTO(BaseModel):
    id: str
    title: str
    order_index: int

class BossDTO(BaseModel):
    id: str
    name: str
    slug: str

class WorldDTO(BaseModel):
    slug: str
    label: str
    tracks: List[TrackDTO]
    bosses: List[BossDTO]

class UniverseResponse(BaseModel):
    worlds: List[WorldDTO]

@router.get("/", response_model=UniverseResponse)
async def get_universe(session: Session = Depends(get_session)):
    """
    Returns the static structure of the known Universe (Worlds -> Tracks/Bosses).
    """
    # 1. Define known worlds (could be in DB, but often hardcoded root objects)
    # We'll support Python and TS
    world_slugs = ["world-python", "world-typescript", "world-java"]
    
    worlds_data = []
    
    for slug in world_slugs:
        # Fetch Tracks
        stmt = (
            select(TrackDefinition)
            .where(TrackDefinition.world_id == slug)
            .order_by(TrackDefinition.order_index)
        )
        tracks = (await session.exec(stmt)).all()
        
        # Fetch Bosses
        b_stmt = (
            select(BossDefinition)
            .where(BossDefinition.world_id == slug)
        )
        bosses = (await session.exec(b_stmt)).all()
        
        if slug == "world-python":
            label = "The Foundry"
        elif slug == "world-typescript":
            label = "The Prism"
        else:
            label = "The Reactor"
        
        worlds_data.append(WorldDTO(
            slug=slug,
            label=label,
            tracks=[
                TrackDTO(id=t.id, title=t.name, order_index=t.order_index) 
                for t in tracks
            ],
            bosses=[
                BossDTO(id=b.id, name=b.name, slug=getattr(b, 'slug', b.id)) 
                for b in bosses
            ]
        ))
        
    return UniverseResponse(worlds=worlds_data)

import json
import os
from typing import List, Dict, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import select, Session

from arcade_app.database import get_session
from arcade_app.models import TrackDefinition, BossDefinition

router = APIRouter(prefix="/api/universe", tags=["universe"])

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_active_worlds() -> list[str]:
    """Read active_worlds from configs/curriculum_guardrail_scope.json."""
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    scope_path = os.path.join(root, "configs", "curriculum_guardrail_scope.json")
    try:
        with open(scope_path, "r", encoding="utf-8") as f:
            return json.load(f).get("active_worlds", ["world-python"])
    except Exception:
        return ["world-python"]

# Canonical world catalogue: slug → display label
_WORLD_CATALOGUE = {
    "world-python":     "The Foundry",
    "world-sql":        "The Query Engine",
    "world-typescript": "The Prism",
    "world-java":       "The Reactor",
    "world-web":        "The Browser",
    "world-js":         "The Node",
    "world-ts":         "The Type System",
    "world-git":        "The Repository",
    "world-agents":     "The Oracle",
}

# ---------------------------------------------------------------------------
# DTOs
# ---------------------------------------------------------------------------

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
    coming_soon: bool
    tracks: List[TrackDTO]
    bosses: List[BossDTO]

class UniverseResponse(BaseModel):
    worlds: List[WorldDTO]

# ---------------------------------------------------------------------------
# Route
# ---------------------------------------------------------------------------

@router.get("", response_model=UniverseResponse)
async def get_universe(session: Session = Depends(get_session)):
    """
    Returns the structure of the known Universe (Worlds -> Tracks/Bosses).

    Only worlds in curriculum_guardrail_scope.json active_worlds have
    coming_soon=False. All others are surfaced as coming_soon=True so the
    UI can style them as placeholders without hiding the roadmap.
    """
    active_worlds = _load_active_worlds()

    # Include active worlds first, then any in the catalogue that have tracks
    candidate_slugs = list(_WORLD_CATALOGUE.keys())

    worlds_data = []

    for slug in candidate_slugs:
        # Fetch Tracks
        stmt = (
            select(TrackDefinition)
            .where(TrackDefinition.world_id == slug)
            .order_by(TrackDefinition.order_index)
        )
        tracks = (await session.exec(stmt)).all()

        # Fetch Bosses
        bosses = (await session.exec(
            select(BossDefinition).where(BossDefinition.world_id == slug)
        )).all()

        coming_soon = slug not in active_worlds

        # Skip worlds with no tracks AND not active (reduces noise)
        if coming_soon and not tracks:
            continue

        worlds_data.append(WorldDTO(
            slug=slug,
            label=_WORLD_CATALOGUE.get(slug, slug),
            coming_soon=coming_soon,
            tracks=[
                TrackDTO(id=t.id, title=t.name, order_index=t.order_index)
                for t in tracks
            ],
            bosses=[
                BossDTO(id=b.id, name=b.name, slug=getattr(b, "slug", b.id))
                for b in bosses
            ],
        ))

    # Sort: active worlds first, then coming soon
    worlds_data.sort(key=lambda w: (w.coming_soon, w.slug))

    return UniverseResponse(worlds=worlds_data)

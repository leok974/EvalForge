from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
import os

router = APIRouter()

# Allow overriding base docs path for flexibility
BASE_DOCS = os.getenv("EVALFORGE_DOCS_ROOT", "d:/EvalForge/docs")

WORLD_LADDER_DOCS = {
    "world-java": "evalforge_reactor_ladder_java.json",
    "world-python": "evalforge_foundry_ladder_python.json",
    "world-typescript": "evalforge_prism_ladder_typescript.json",
    "world-sql": "evalforge_archives_ladder_sql.json",
    "world-infra": "evalforge_grid_ladder_infra.json",
    "world-agents": "evalforge_oracle_ladder_agents.json",
    "world-git": "evalforge_timeline_ladder_git.json",
    "world-ml": "evalforge_synapse_ladder_ml.json",
}

@router.get("/api/worlds/{world_slug}/ladder", tags=["ladder"])
def get_world_ladder(world_slug: str):
    filename = WORLD_LADDER_DOCS.get(world_slug)
    
    if not filename:
         # Implicit 404 for worlds without ladders defined yet
         raise HTTPException(status_code=404, detail=f"No ladder defined for world: {world_slug}")
         
    target_file = Path(BASE_DOCS) / filename
    
    if not target_file.exists():
        raise HTTPException(status_code=404, detail="Ladder spec file not found on disk")
        
    try:
        data = json.loads(target_file.read_text(encoding="utf-8"))
        return data.get("ladder", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load ladder spec: {str(e)}")

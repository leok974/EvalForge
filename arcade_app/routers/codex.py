from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from arcade_app.codex_helper import index_codex, get_codex_entry

router = APIRouter(prefix="/api/codex", tags=["codex"])

@router.get("")
async def list_codex_entries(
    world: Optional[str] = None, 
    world_id: Optional[str] = None,
    source: Optional[str] = None
):
    """
    List all codex entries, optionally filtered by world or source.
    """
    entries = index_codex()
    
    # Handle world/world_id alias
    target_world = world or world_id
    
    if target_world and target_world.lower() != "all":
        entries = [e for e in entries if e.get("world") == target_world or e.get("world") == "general"]
        
    if source:
         entries = [e for e in entries if e.get("source") == source]
        
    return entries

@router.get("/{entry_id}")
async def get_codex_entry_detail(entry_id: str):
    """
    Get full content for a specific codex entry.
    """
    entry = get_codex_entry(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Codex entry not found")
    return entry

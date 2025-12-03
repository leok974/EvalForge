from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from arcade_app.codex_helper import index_codex, get_codex_entry
from arcade_app.database import get_session
from sqlmodel import select
from arcade_app.models import KnowledgeChunk, Project

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
    # 1. File-based entries
    entries = index_codex()
    
    # 2. DB-based entries (Project Docs)
    if source != "core": # Skip if only asking for core
        async for session in get_session():
            stmt = select(KnowledgeChunk, Project).where(KnowledgeChunk.source_type == "project").where(KnowledgeChunk.source_id == Project.id)
            results = await session.execute(stmt)
            for chunk, proj in results:
                # Try to parse frontmatter for doc_type
                title = f"{proj.name}: Documentation"
                doc_type = None
                
                if chunk.content.startswith("---"):
                    try:
                        # Extract frontmatter
                        parts = chunk.content.split("---", 2)
                        if len(parts) >= 3:
                            import yaml
                            frontmatter = yaml.safe_load(parts[1])
                            if frontmatter and isinstance(frontmatter, dict):
                                doc_type = frontmatter.get("doc_type", "").capitalize()
                                if doc_type:
                                    title = f"{proj.name}: {doc_type}"
                    except Exception as e:
                        print(f"Failed to parse frontmatter for chunk {chunk.id}: {e}")
                
                entries.append({
                    "id": f"db-{chunk.id}",
                    "title": title,
                    "world": proj.default_world_id,
                    "world_id": proj.default_world_id,
                    "tags": ["project", proj.name] + ([doc_type.lower()] if doc_type else []),
                    "source": "project",
                    "project_id": proj.id,
                    "doc_type": doc_type.lower() if doc_type else None
                })

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
    # 1. Try DB first if it looks like a DB ID
    if entry_id.startswith("db-"):
        try:
            db_id = int(entry_id.replace("db-", ""))
            async for session in get_session():
                chunk = await session.get(KnowledgeChunk, db_id)
                if chunk:
                    proj = await session.get(Project, chunk.source_id)
                    return {
                        "metadata": {
                            "id": entry_id,
                            "title": f"{proj.name}: Documentation",
                            "world": proj.default_world_id,
                            "tags": ["project", proj.name],
                            "source": "project"
                        },
                        "content": chunk.content
                    }
        except Exception as e:
            print(f"DB Codex Error: {e}")
            pass

    # 2. Fallback to File System
    entry = get_codex_entry(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Codex entry not found")
    return entry

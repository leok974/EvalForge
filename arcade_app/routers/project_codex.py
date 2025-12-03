from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from arcade_app.database import get_session
from sqlmodel import select
from arcade_app.models import Project, ProjectCodexDoc

router = APIRouter(prefix="/api/project_codex", tags=["project_codex"])

@router.get("/projects")
async def list_projects():
    """
    List all synced projects with summary info for the Project Codex index.
    
    Returns:
        List[ProjectCodexSummary]: Project summaries with available doc types
    """
    projects = []
    
    async for session in get_session():
        # Get all projects
        stmt = select(Project)
        result = await session.execute(stmt)
        all_projects = result.scalars().all()
        
        for proj in all_projects:
            # Get all docs for this project to determine available doc_types
            doc_stmt = select(ProjectCodexDoc).where(
                ProjectCodexDoc.project_id == proj.id
            )
            doc_result = await session.execute(doc_stmt)
            docs = doc_result.scalars().all()
            
            # Extract doc_types
            doc_types = [doc.doc_type for doc in docs]
            
            # Collect worlds from all docs
            worlds_set = set([proj.default_world_id])
            for doc in docs:
                if doc.world_ids:
                    worlds_set.update(doc.world_ids)
            
            # Extract tagline from summary_data or use default
            tagline = proj.summary_data.get("tagline", f"A {proj.summary_data.get('primary_language', 'software')} project") if proj.summary_data else ""
            
            # Build tags from stack
            tags = proj.summary_data.get("stack", []) if proj.summary_data else []
            
            projects.append({
                "slug": proj.name.lower().replace(" ", "-"),
                "name": proj.name,
                "tagline": tagline,
                "worlds": list(worlds_set),
                "tags": tags,
                "doc_types": doc_types,
                "codex_status": proj.codex_status or "missing_docs"
            })
    
    return projects


@router.get("/projects/{slug}")
async def get_project_bundle(slug: str):
    """
    Get all documentation for a specific project.
    
    Args:
        slug: Project slug (e.g., "applylens")
        
    Returns:
        ProjectCodexBundle: Project summary + all docs
    """
    async for session in get_session():
        # Find project by slug (case-insensitive match on name)
        stmt = select(Project)
        result = await session.execute(stmt)
        projects = result.scalars().all()
        
        # Match by slug
        proj = None
        for p in projects:
            if p.name.lower().replace(" ", "-") == slug.lower():
                proj = p
                break
        
        if not proj:
            raise HTTPException(status_code=404, detail=f"Project '{slug}' not found")
        
        # Get all docs for this project
        doc_stmt = select(ProjectCodexDoc).where(
            ProjectCodexDoc.project_id == proj.id
        )
        
        doc_result = await session.execute(doc_stmt)
        db_docs = doc_result.scalars().all()
        
        # Format docs
        docs = []
        worlds_set = set([proj.default_world_id])
        
        for doc in db_docs:
            if doc.world_ids:
                worlds_set.update(doc.world_ids)
                
            docs.append({
                "doc_type": doc.doc_type,
                "title": doc.title,
                "body_md": doc.body_md,
                "tags": doc.tags or []
            })
        
        # Build project summary
        tagline = proj.summary_data.get("tagline", "") if proj.summary_data else ""
        stack_tags = proj.summary_data.get("stack", []) if proj.summary_data else []
        
        project_summary = {
            "slug": slug,
            "name": proj.name,
            "tagline": tagline,
            "worlds": list(worlds_set),
            "tags": stack_tags,
            "doc_types": [d["doc_type"] for d in docs],
            "codex_status": proj.codex_status or "missing_docs"
        }
        
        return {
            "project": project_summary,
            "docs": docs
        }

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from pydantic import BaseModel
from arcade_app.auth_helper import get_current_user
from arcade_app.project_helper import list_projects, create_project, sync_project

router = APIRouter(prefix="/api/projects", tags=["projects"])

class CreateProjectRequest(BaseModel):
    repo_url: str

@router.get("", response_model=List[Dict[str, Any]])
async def list_my_projects(
    current_user: Dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return await list_projects(current_user["id"])

@router.post("", response_model=Dict[str, Any])
async def add_project(
    payload: CreateProjectRequest,
    current_user: Dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        return await create_project(current_user["id"], payload.repo_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{project_id}/sync")
async def sync_project_endpoint(
    project_id: str,
    background_tasks: BackgroundTasks,
    current_user: Dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # For now, we run sync in background task (simple async)
    # In production, this should go to Celery/Redis Queue
    background_tasks.add_task(sync_project, project_id)
    
    return {"status": "sync_started", "project_id": project_id}


@router.post("/{project_slug}/questline/generate")
async def generate_project_questline_endpoint(
    project_slug: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Generate a project-specific questline using QuestMaster.
    For ApplyLens, set QUESTMASTER_GOLDEN_APPLYLENS=1 to use the golden spec.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    from arcade_app.database import get_session
    from arcade_app.models import Project
    from arcade_app.questmaster import generate_project_questline
    from arcade_app.project_questline_apply import apply_project_questline_spec
    from sqlmodel import select
    
    async for session in get_session():
        # Find project
        project = (await session.exec(
            select(Project).where(
                Project.slug == project_slug,
                Project.owner_user_id == current_user["id"]
            )
        )).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Generate questline spec
        try:
            spec = generate_project_questline(session, project)
        except NotImplementedError as e:
            raise HTTPException(status_code=501, detail=str(e))
        
        # Apply to database
        def apply_sync(conn):
            from sqlmodel import Session
            sync_session = Session(bind=conn)
            apply_project_questline_spec(sync_session, spec)
        
        async with session.begin() as conn:
            await conn.run_sync(apply_sync)
        
        return spec.dict()

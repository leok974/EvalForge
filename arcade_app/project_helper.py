from datetime import datetime
from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import Project
from arcade_app.ingestion_helper import ingest_project_repo
import re

async def list_projects(user_id: str) -> list[dict]:
    async for session in get_session():
        statement = select(Project).where(Project.owner_user_id == user_id)
        result = await session.execute(statement)
        projects = result.scalars().all()
        return [p.model_dump() for p in projects]

async def create_project(user_id: str, repo_url: str) -> dict:
    # 1. Validate GitHub URL
    repo_url = repo_url.strip()
    github_pattern = r'^https?://github\.com/[\w-]+/[\w.-]+/?$'
    if not re.match(github_pattern, repo_url):
        raise ValueError(f"Invalid GitHub URL: {repo_url}. Must be in format: https://github.com/username/repo")
    
    # 2. Check for duplicates
    async for session in get_session():
        existing = await session.execute(
            select(Project).where(
                Project.owner_user_id == user_id,
                Project.repo_url == repo_url
            )
        )
        if existing.scalar_one_or_none():
            raise ValueError(f"Project already exists: {repo_url}")
    
    # 3. Parse Name & Guess World
    name = repo_url.rstrip("/").split("/")[-1]
    world = "world-infra"
    if "backend" in name or "api" in name: world = "world-python"
    elif "web" in name or "ui" in name: world = "world-js"

    new_proj = Project(
        owner_user_id=user_id,
        name=name,
        repo_url=repo_url,
        default_world_id=world,
        summary_data={},
        sync_status="pending"
    )
    
    # 4. Insert into DB
    async for session in get_session():
        session.add(new_proj)
        await session.commit()
        await session.refresh(new_proj)
        return new_proj.model_dump()

async def sync_project(project_id: str) -> dict:
    async for session in get_session():
        proj = await session.get(Project, project_id)
        if not proj:
            return {}
        
        # 1. Update Status to 'Syncing'
        proj.sync_status = "syncing"
        session.add(proj)
        await session.commit()
        
        # 2. Run Ingestion (Ideally this should be a background task/worker)
        # For MVP, we await it (might take 10-20s for small repos)
        result = await ingest_project_repo(proj.id, proj.repo_url)
        
        # 3. Update Final Status
        if result["status"] == "ok":
            proj.sync_status = "ok"
            proj.last_sync_at = datetime.utcnow()
            
            # Stack detection logic
            stack = []
            if "python" in proj.default_world_id:
                stack = ["fastapi", "postgres"]
            elif "js" in proj.default_world_id:
                stack = ["react", "vite"]
                
            proj.summary_data = {
                "primary_language": "python" if "python" in proj.default_world_id else "typescript",
                "stack": stack,
                "files_indexed": result.get("files_indexed", 0)
            }
        else:
            proj.sync_status = "error"
            proj.summary_data = {"error": result.get("message", "Unknown error")}
            
        session.add(proj)
        await session.commit()
        await session.refresh(proj)
        return proj.model_dump()

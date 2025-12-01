from langchain_core.tools import tool
from arcade_app.rag_helper import search_knowledge
from arcade_app.project_helper import list_projects, create_project, sync_project

@tool
async def list_my_projects(user_id: str):
    """
    Lists all GitHub repositories currently linked to the user's account.
    Returns the project Name, ID, Sync Status, and Last Sync timestamp.
    """
    try:
        projs = await list_projects(user_id)
        if not projs:
            return "No projects linked. Recommend using 'add_my_project' to link a repository."
        
        report = "## PROJECT REGISTRY STATUS\n"
        for p in projs:
            last = p.get('last_sync_at')
            last_str = str(last).split('.')[0] if last else 'Never'
            report += f"- **{p['name']}** (`{p['id']}`)\n  - Status: {p['sync_status'].upper()}\n  - Last Sync: {last_str}\n  - Stack: {', '.join(p.get('summary_data', {}).get('stack', []))}\n"
        return report
    except Exception as e:
        return f"Error listing projects: {str(e)}"

@tool
async def add_my_project(user_id: str, repo_url: str):
    """
    Links a new GitHub repository URL to the system.
    This action creates the project entry and immediately triggers an initial sync/ingestion.
    """
    try:
        proj = await create_project(user_id, repo_url)
        # Trigger Sync (fire-and-forget logic handled inside sync_project usually, here we await)
        await sync_project(proj["id"])
        
        return f"✅ **LINK ESTABLISHED**\nProject: {proj['name']}\nID: {proj['id']}\nStatus: SYNC INITIATED."
    except Exception as e:
        return f"❌ Failed to link project: {str(e)}"

@tool
async def sync_my_project(user_id: str, project_name_or_id: str):
    """
    Triggers a re-ingestion/sync for an existing project.
    Use this if the user asks to 'update', 'refresh', or 'sync' a specific repo.
    """
    try:
        projs = await list_projects(user_id)
        # Fuzzy match name or ID
        target = next((p for p in projs if p['id'] == project_name_or_id or p['name'] == project_name_or_id), None)
        
        if not target:
            return f"❌ Project '{project_name_or_id}' not found in registry."
        
        await sync_project(target["id"])
        return f"🔄 **SYNC PROTOCOL INITIATED**\nTarget: {target['name']}\nBackground workers dispatched."
    except Exception as e:
        return f"❌ Sync failed: {str(e)}"

# Export list for Graph binding
REGISTRY_TOOLS = [list_my_projects, add_my_project, sync_my_project]

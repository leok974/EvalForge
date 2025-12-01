import pytest
from unittest.mock import AsyncMock, patch
from arcade_app.tools import list_my_projects, add_my_project, sync_my_project

# Mark async tests
pytestmark = pytest.mark.asyncio

async def test_list_projects_empty():
    """Verify friendly message when no projects exist."""
    with patch("arcade_app.tools.list_projects", new_callable=AsyncMock) as mock_list:
        mock_list.return_value = []
        
        result = await list_my_projects.ainvoke("user_1")
        assert "No projects linked" in result

async def test_list_projects_formatted():
    """Verify the list tool returns a Markdown table/list."""
    mock_data = [{
        "id": "p1", "name": "my-repo", "sync_status": "ok", 
        "last_sync_at": "2023-01-01", "summary_data": {"stack": ["python"]}
    }]
    
    with patch("arcade_app.tools.list_projects", new_callable=AsyncMock) as mock_list:
        mock_list.return_value = mock_data
        
        result = await list_my_projects.ainvoke("user_1")
        assert "PROJECT REGISTRY STATUS" in result
        assert "**my-repo**" in result
        assert "OK" in result

async def test_add_project_success():
    """Verify adding a project triggers sync and returns success."""
    mock_proj = {"id": "p_new", "name": "new-repo"}
    
    with patch("arcade_app.tools.create_project", new_callable=AsyncMock) as mock_create, \
         patch("arcade_app.tools.sync_project", new_callable=AsyncMock) as mock_sync:
        
        mock_create.return_value = mock_proj
        mock_sync.return_value = {} # Return doesn't matter for tool wrapper
        
        result = await add_my_project.ainvoke({"user_id": "u1", "repo_url": "http://github/new"})
        
        assert "LINK ESTABLISHED" in result
        assert "new-repo" in result
        mock_sync.assert_called_once_with("p_new")

async def test_sync_project_lookup_fail():
    """Verify error handling when project is not found."""
    with patch("arcade_app.tools.list_projects", new_callable=AsyncMock) as mock_list:
        mock_list.return_value = [{"id": "p1", "name": "existing"}]
        
        result = await sync_my_project.ainvoke({"user_id": "u1", "project_name_or_id": "ghost-repo"})
        assert "not found" in result

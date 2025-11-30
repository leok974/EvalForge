import pytest
from sqlmodel import select
from arcade_app.models import User, Profile, Project
from arcade_app.profile_helper import add_xp, get_profile
from arcade_app.project_helper import create_project, list_projects, sync_project

# Mark all tests as async
pytestmark = pytest.mark.asyncio

async def test_create_user_and_profile_automatically(db_session):
    # 1. Calling get_profile for non-existent user should create them
    data = await get_profile("test_user")
    
    assert data["total_xp"] == 0
    assert data["level"] == 1
    
    # 2. Verify in DB
    user = await db_session.get(User, "test_user")
    assert user is not None
    assert user.name == "test_user (Dev)"

async def test_add_xp_logic(db_session):
    # 1. Award XP
    # This should create the user AND award XP in one go
    result = await add_xp("gamer", "world-python", 150)
    
    assert result["xp_gained"] == 150
    assert result["new_world_level"] == 2 # 150 XP > 100 threshold
    assert result["world_level_up"] is True
    
    # 2. Check persistence
    profile_data = await get_profile("gamer")
    assert profile_data["total_xp"] == 150
    assert profile_data["world_progress"]["world-python"]["xp"] == 150

async def test_create_project(db_session):
    # 1. Create User first (Foreign Key constraint)
    user = User(id="leo", name="Leo")
    db_session.add(user)
    await db_session.commit()
    
    # 2. Create Project
    proj = await create_project("leo", "https://github.com/leo/cool-api")
    
    assert proj["name"] == "cool-api"
    assert proj["default_world_id"] == "world-python" # Auto-detected from 'api'
    assert proj["owner_user_id"] == "leo"
    
    # 3. List
    projs = await list_projects("leo")
    assert len(projs) == 1
    assert projs[0]["name"] == "cool-api"

async def test_sync_project(db_session):
    # Setup
    user = User(id="leo", name="Leo")
    db_session.add(user)
    await db_session.commit()
    
    p_data = await create_project("leo", "https://github.com/leo/frontend-ui")
    
    # Sync
    synced = await sync_project(p_data["id"])
    
    assert synced["sync_status"] == "ok"
    # Should detect JS/React based on 'ui' name
    assert synced["summary_data"]["primary_language"] == "typescript"

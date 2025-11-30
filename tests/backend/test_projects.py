import os
import json
import pytest
import shutil
from arcade_app import project_helper

TEST_DATA_DIR = "tests/data_temp"
TEST_PROJECTS_FILE = f"{TEST_DATA_DIR}/projects.json"

@pytest.fixture(autouse=True)
def mock_project_db():
    # Setup: Create temp dir and override file path
    os.makedirs(TEST_DATA_DIR, exist_ok=True)
    with open(TEST_PROJECTS_FILE, "w") as f:
        json.dump([], f)
    
    original_file = project_helper.PROJECTS_FILE
    project_helper.PROJECTS_FILE = TEST_PROJECTS_FILE
    
    yield
    
    # Teardown
    project_helper.PROJECTS_FILE = original_file
    shutil.rmtree(TEST_DATA_DIR)

def test_create_and_list_project():
    # 1. Create
    p = project_helper.create_project("leo", "https://github.com/leo/my-api")
    assert p["name"] == "my-api"
    assert p["owner_user_id"] == "leo"
    assert p["sync_status"] == "pending"
    assert p["default_world_id"] == "world-python" # inferred from 'api'
    
    # 2. List
    projs = project_helper.list_projects("leo")
    assert len(projs) == 1
    assert projs[0]["id"] == p["id"]

def test_list_filters_by_user():
    project_helper.create_project("leo", "http://gh.com/leo/p1")
    project_helper.create_project("other", "http://gh.com/other/p2")
    
    leo_projs = project_helper.list_projects("leo")
    assert len(leo_projs) == 1
    assert leo_projs[0]["name"] == "p1"

def test_sync_project():
    # Create project
    p = project_helper.create_project("leo", "https://github.com/leo/web-ui")
    assert p["summary"] == {}
    
    # Sync
    synced = project_helper.sync_project(p["id"])
    assert synced["sync_status"] == "ok"
    assert synced["last_sync_at"] is not None
    # 'web-ui' should map to JS world -> React stack
    assert "react" in synced["summary"]["stack"]

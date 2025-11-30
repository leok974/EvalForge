import os
import pytest
import shutil
from fastapi.testclient import TestClient
from arcade_app.agent import app
from arcade_app import codex_helper

client = TestClient(app)

# Fixture: Create a fake Codex directory for testing
@pytest.fixture(autouse=True)
def mock_codex_dir():
    # Setup
    test_dir = "tests/data_temp/codex"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create a dummy markdown file
    with open(f"{test_dir}/test-entry.md", "w") as f:
        f.write("---\nid: test-entry\ntitle: Test Title\nworld: world-python\ntags: [test]\n---\n# Content")
    
    # Override the path in the helper module dynamically
    original_dir = codex_helper.CODEX_DIR
    codex_helper.CODEX_DIR = test_dir
    
    yield
    
    # Teardown
    codex_helper.CODEX_DIR = original_dir
    shutil.rmtree("tests/data_temp")

def test_index_codex():
    response = client.get("/api/codex")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "test-entry"
    assert data[0]["world"] == "world-python"

def test_filter_codex():
    # Should find it
    res1 = client.get("/api/codex?world=world-python")
    assert len(res1.json()) == 1
    
    # Should NOT find it
    res2 = client.get("/api/codex?world=world-java")
    assert len(res2.json()) == 0

def test_read_entry():
    response = client.get("/api/codex/test-entry")
    assert response.status_code == 200
    assert "# Content" in response.json()["content"]

def test_read_missing_entry():
    response = client.get("/api/codex/fake-id")
    assert response.status_code == 404

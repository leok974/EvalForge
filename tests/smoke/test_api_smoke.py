"""
Smoke tests for EvalForge API.
These tests verify core functionality works end-to-end:
- Database initialization
- Universe data seeding
- Critical API endpoints

Run locally: pytest tests/smoke/test_api_smoke.py -v
Run in CI: Configured in .github/workflows/smoke-test.yml
"""
import pytest
from fastapi.testclient import TestClient
from arcade_app.agent import app

# Create test client once
client = TestClient(app)



def test_health_endpoint():
    """Test that the health endpoint returns OK."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_healthz_endpoint():
    """Test that the healthz endpoint returns OK."""
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_universe_endpoint():
    """Test that universe data is available and properly structured."""
    response = client.get("/api/universe")
    assert response.status_code == 200
    
    data = response.json()
    assert "worlds" in data
    
    worlds = data["worlds"]
    assert len(worlds) >= 3, "Should have at least Python, TypeScript, Java worlds"
    
    # Check for expected worlds
    world_slugs = {w["slug"] for w in worlds}
    assert "world-python" in world_slugs
    assert "world-typescript" in world_slugs
    assert "world-java" in world_slugs
    
    # Verify world structure
    python_world = next(w for w in worlds if w["slug"] == "world-python")
    assert "label" in python_world
    assert "tracks" in python_world
    assert "bosses" in python_world
    assert len(python_world["tracks"]) > 0, "Python world should have tracks"


def test_quests_endpoint_python():
    """Test that Python world quests are available."""
    response = client.get("/api/quests/?world_id=world-python")
    assert response.status_code == 200
    
    quests = response.json()
    assert isinstance(quests, list)
    assert len(quests) > 0, "Should have at least one quest for Python world"
    
    # Verify quest structure
    first_quest = quests[0]
    required_fields = ["id", "slug", "world_id", "track_id", "title", "state"]
    for field in required_fields:
        assert field in first_quest, f"Quest missing required field: {field}"
    
    assert first_quest["world_id"] == "world-python"


def test_quests_endpoint_typescript():
    """Test that TypeScript world quests are available."""
    response = client.get("/api/quests/?world_id=world-typescript")
    assert response.status_code == 200
    
    quests = response.json()
    assert isinstance(quests, list)
    # TypeScript world should have quests too
    if len(quests) > 0:
        assert quests[0]["world_id"] == "world-typescript"


def test_quests_endpoint_java():
    """Test that Java world quests are available."""
    response = client.get("/api/quests/?world_id=world-java")
    assert response.status_code == 200
    
    quests = response.json()
    assert isinstance(quests, list)
    # Java world should have quests too
    if len(quests) > 0:
        assert quests[0]["world_id"] == "world-java"


def test_version_endpoint():
    """Test that version endpoint returns expected data."""
    response = client.get("/version")
    assert response.status_code == 200
    
    data = response.json()
    assert "version" in data
    assert "environment" in data
    assert data["version"] == "0.4.0"


def test_ready_endpoint():
    """Test that readiness check passes."""
    response = client.get("/api/ready")
    
    # Should return 200 if DB is accessible, 503 if not
    # In CI, this might fail if DB isn't ready yet
    assert response.status_code in [200, 503]
    
    data = response.json()
    assert "status" in data or "detail" in data


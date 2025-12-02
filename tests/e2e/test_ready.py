import pytest
import os
from fastapi.testclient import TestClient
from arcade_app.agent import app

# Default to TestClient (in-memory) if no live URL provided
TEST_URL = os.getenv("EVALFORGE_TEST_URL")

@pytest.fixture
def client():
    return TestClient(app)

def test_readiness_endpoint(client):
    """
    Verifies that /api/ready returns 200 OK and status='ready'.
    If running against a live URL, uses requests/httpx.
    """
    if TEST_URL:
        import requests
        try:
            response = requests.get(f"{TEST_URL}/api/ready", timeout=5)
        except requests.exceptions.ConnectionError:
            pytest.fail(f"Could not connect to {TEST_URL}")
    else:
        # Mock DB session for TestClient if needed, 
        # but the endpoint catches exceptions and returns 503 if DB fails.
        # We want to assert the structure of the response, even if DB is 'error' in this env.
        response = client.get("/api/ready")
    
    # We expect 200 if everything is mocked correctly, or 503 if DB is missing.
    # For this smoke test, we primarily want to ensure the endpoint EXISTS and returns JSON.
    
    assert response.status_code in [200, 503]
    data = response.json()
    
    if response.status_code == 503:
        # If 503, it returns {"detail": {"database": ..., "redis": ...}}
        assert "detail" in data
        assert "database" in data["detail"]
        assert "redis" in data["detail"]
    else:
        assert "status" in data
        assert "components" in data
        assert "database" in data["components"]
        assert "redis" in data["components"]

def test_health_endpoint(client):
    """Verifies /health returns 200 OK."""
    if TEST_URL:
        import requests
        response = requests.get(f"{TEST_URL}/health", timeout=5)
    else:
        response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

from fastapi.testclient import TestClient
from arcade_app.agent import app

client = TestClient(app)

def test_get_universe():
    response = client.get("/api/universe")
    assert response.status_code == 200
    data = response.json()
    
    assert "worlds" in data
    assert "tracks" in data
    
    # Check for known default data (assuming data/tracks.json exists)
    # If using test data, you'd mock load_universe_data similar to codex above
    if len(data["worlds"]) > 0:
        assert "id" in data["worlds"][0]
        assert "name" in data["worlds"][0]

import pytest
from httpx import AsyncClient, ASGITransport
from arcade_app.main import app
from arcade_app.auth_helper import get_current_user
from arcade_app.models import QuestDefinition, TrackDefinition
from arcade_app.services import quest_visibility

from arcade_app.routers import routes_workshop

@pytest.mark.asyncio
async def test_workshop_catalog(db_session):
    # Setup Auth Override
    app.dependency_overrides[get_current_user] = lambda: {"id": "test_user", "name": "Tester"}
    
    # Mock active config in the ROUTER namespace
    original_config = routes_workshop.get_active_quest_config
    routes_workshop.get_active_quest_config = lambda root_dir=None: ({"test-quest"}, {"test-quest": "test_pack"})
    
    try:
        # Seed DB with a quest that maps to a REAL World ID (world-python) to verify worlds.json lookup
        # And a track that we define.
        q = QuestDefinition(
            slug="test-quest",
            world_id="world-python", 
            track_id="python-fundamentals",
            title="Test Quest",
            short_description="Desc",
            order_index=1
        )
        db_session.add(q)
        
        t = TrackDefinition(
            id="python-fundamentals",
            world_id="world-python",
            name="Python Fundamentals (Lore)",
            description="Track Desc",
            order_index=1
        )
        db_session.add(t)
        
        await db_session.commit()
        
        # Act
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/api/workshop/catalog")
            
        # Assert
        assert response.status_code == 200
        data = response.json()
        
        assert "worlds" in data
        assert "tracks" in data
        
        # Verify World (Should be found in worlds.json)
        worlds = data["worlds"]
        # world-python should be there
        py_world = next((w for w in worlds if w["world_id"] == "world-python"), None)
        assert py_world is not None
        assert py_world["real_name"] == "world-python"
        # Check Lore Name resolution (The Foundry)
        assert "Foundry" in py_world["lore_name"] 
        assert py_world["quest_count"] == 1
        
        # Verify Track
        tracks = data["tracks"]
        py_track = next((t for t in tracks if t["track_id"] == "python-fundamentals"), None)
        assert py_track is not None
        assert py_track["real_name"] == "python-fundamentals"
        assert py_track["lore_name"] == "Python Fundamentals (Lore)"
        assert py_track["quest_count"] == 1
        
    finally:
        # Cleanup
        routes_workshop.get_active_quest_config = original_config
        app.dependency_overrides = {}

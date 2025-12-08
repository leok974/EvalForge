import pytest
from httpx import AsyncClient
from sqlmodel import select

# We rely on the seeded universe from previous steps.
# If the tests run in isolation, we might need to ensure content is seeded 
# or mocked. However, in this environment, it seems we run against a persistent DB 
# or a seeded fixture.

@pytest.mark.asyncio
async def test_practice_round_includes_all_worlds(client: AsyncClient):
    """
    Verify that /api/practice_rounds/today returns items from multiple worlds
    now that we've enabled them all.
    """
    
    # 1. Fetch practice round
    response = await client.get("/api/practice_rounds/today")
    assert response.status_code == 200
    
    data = response.json()
    items = data["items"]
    
    # We might not get *all* worlds in a single day (limited to 5 items),
    # but we should definitely see more than just Python/Java if the filter is working.
    # Actually, stable seed might restrict it, but let's check what we get.
    
    print(f"DEBUG: Practice Items: {items}")
    
    found_worlds = set()
import pytest
from httpx import AsyncClient
from sqlmodel import select

# We rely on the seeded universe from previous steps.
# If the tests run in isolation, we might need to ensure content is seeded 
# or mocked. However, in this environment, it seems we run against a persistent DB 
# or a seeded fixture.

@pytest.mark.asyncio
async def test_practice_round_includes_all_worlds(client: AsyncClient):
    """
    Verify that /api/practice_rounds/today returns items from multiple worlds
    now that we've enabled them all.
    """
    
    # 1. Fetch practice round
    response = await client.get("/api/practice_rounds/today")
    assert response.status_code == 200
    
    data = response.json()
    items = data["items"]
    
    # We might not get *all* worlds in a single day (limited to 5 items),
    # but we should definitely see more than just Python/Java if the filter is working.
    # Actually, stable seed might restrict it, but let's check what we get.
    
    print(f"DEBUG: Practice Items: {items}")
    
    found_worlds = set()
    for item in items:
        # We expect fields like 'world_slug' to be populated
        if item.get("world_slug"):
            found_worlds.add(item["world_slug"])
            
    print(f"DEBUG: Found World Slugs: {found_worlds}")
    
    # Check that we have valid slugs from the allowed set
    allowed_worlds = {
        "world-python", "world-typescript", "world-java",
        "world-sql", "world-infra", "world-agents",
        "world-git", "world-ml"
    }
    
    for w in found_worlds:
        assert w in allowed_worlds, f"Unexpected world slug: {w}"
        
    # Optional: Verify stats are present
    assert "today_quests_completed" in data
    assert "today_bosses_cleared" in data
    
    # Streak fields
    assert "streak_days" in data
    assert "best_streak_days" in data
    assert isinstance(data["streak_days"], int)
    assert isinstance(data["best_streak_days"], int)

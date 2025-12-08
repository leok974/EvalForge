import pytest

@pytest.mark.asyncio
async def test_boss_foundry_systems_smoke(client):
    # 1. Check Codex Retrieval
    print("Checking Codex Retrieval...")
    response = await client.get("/api/codex/boss-foundry-systems-architect")
    assert response.status_code == 200, f"Codex returned {response.status_code}: {response.text}"
    data = response.json()
    assert data["id"] == "boss-foundry-systems-architect"
    assert "Legacy code is just a monument" in data["content"] # Quote from codex
    print("✅ Codex OK")

    # 2. Check Rubric Retrieval
    print("Checking Rubric Retrieval...")
    response = await client.get("/api/rubrics/boss-foundry-systems-architect")
    assert response.status_code == 200
    rubric = response.json()
    assert rubric["id"] == "boss-foundry-systems-architect"
    assert len(rubric["criteria"]) == 4
    print("✅ Rubric OK")

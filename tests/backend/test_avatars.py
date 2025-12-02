import pytest
from httpx import AsyncClient
from sqlmodel import select
from arcade_app.models import AvatarDefinition, User

# Note: These tests assume the seed script has been run or fixtures populate the DB

@pytest.mark.asyncio
async def test_list_avatars_includes_lock_and_equip(async_client: AsyncClient, test_user: User, db_session):
    # 1. Fetch avatars
    resp = await async_client.get("/api/avatars")
    assert resp.status_code == 200
    data = resp.json()
    assert "avatars" in data
    
    # 2. Verify Default Avatar (should be equipped for new user)
    default = next((a for a in data["avatars"] if a["id"] == "default_user"), None)
    assert default is not None
    assert default["is_equipped"] is True
    assert default["is_locked"] is False

    # 3. Verify High Level Avatar (should be locked)
    # Assuming 'void_walker' requires level 50 and test_user is level 1
    legendary = next((a for a in data["avatars"] if a["id"] == "void_walker"), None)
    if legendary:
        assert legendary["is_locked"] is True
        assert legendary["is_equipped"] is False

@pytest.mark.asyncio
async def test_equip_avatar_success(async_client: AsyncClient, test_user: User):
    # 1. Equip a common avatar (level 1)
    # 'coder_green' requires level 2, so let's try 'default_user' again or ensure we have a lvl 1 alt
    # Actually, let's try to equip 'default_user' which is definitely unlocked
    
    resp = await async_client.post(
        "/api/avatars/equip", 
        json={"avatar_id": "default_user"}
    )
    assert resp.status_code == 200
    assert resp.json()["current_avatar_id"] == "default_user"

@pytest.mark.asyncio
async def test_cannot_equip_locked_avatar(async_client: AsyncClient):
    # 1. Try to equip a legendary avatar
    resp = await async_client.post(
        "/api/avatars/equip", 
        json={"avatar_id": "void_walker"}
    )
    # Should be 403 Forbidden
    assert resp.status_code == 403
    assert "requires level" in resp.json()["detail"]

@pytest.mark.asyncio
async def test_equip_nonexistent_avatar(async_client: AsyncClient):
    resp = await async_client.post(
        "/api/avatars/equip", 
        json={"avatar_id": "ghost_in_the_machine_999"}
    )
    assert resp.status_code == 404

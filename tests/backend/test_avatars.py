import pytest
import pytest_asyncio
from sqlmodel import select
from sqlalchemy import update, text
from arcade_app.models import User, Profile, AvatarDefinition, AvatarVisualType
from arcade_app.avatar_helper import list_avatars, equip_avatar

# Mark all async tests
pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture
async def avatar_setup(db_session):
    """Seeds the DB with test avatars and a user."""
    # Explicit cleanup to handle SQLite locking/state issues
    # Delete dependent tables first!
    r1 = await db_session.execute(text("DELETE FROM userbadge"))
    r2 = await db_session.execute(text("DELETE FROM usermetric"))
    r3 = await db_session.execute(text("DELETE FROM useravatar"))
    r4 = await db_session.execute(text("DELETE FROM profile"))
    r5 = await db_session.execute(text("DELETE FROM user"))
    r6 = await db_session.execute(text("DELETE FROM avatardefinition"))
    await db_session.commit()
    
    print(f"DEBUG: Deleted rows: {r1.rowcount}, {r2.rowcount}, {r3.rowcount}, {r4.rowcount}, {r5.rowcount}, {r6.rowcount}")

    # 1. Create Avatars
    avatars = [
        AvatarDefinition(id="noob", name="Noob", description="Basic avatar", required_level=1, visual_type="icon", visual_data="user"),
        AvatarDefinition(id="mid", name="Mid", description="Mid avatar", required_level=2, visual_type="icon", visual_data="code"),
        AvatarDefinition(id="pro", name="Pro", description="Pro avatar", required_level=10, visual_type="icon", visual_data="star")
    ]
    for av in avatars:
        db_session.add(av)
    
    # 2. Create User (Level 5)
    user = User(id="player1", name="Player One", current_avatar_id="noob")
    profile = Profile(user_id="player1", total_xp=5000, global_level=5)
    
    db_session.add(user)
    db_session.add(profile)
    await db_session.commit()
    
    # CRITICAL: Detach objects from session so subsequent fetches don't use stale cache
    db_session.expire_all()

async def test_list_avatars_locking(db_session, avatar_setup):
    """Verify that 'Pro' avatar is locked for a Level 5 user."""
    result = await list_avatars("player1")
    
    noob = next(a for a in result if a["id"] == "noob")
    pro = next(a for a in result if a["id"] == "pro")
    
    assert noob["is_locked"] is False
    assert noob["is_equipped"] is True
    assert pro["is_locked"] is True

async def test_equip_success(db_session, avatar_setup):
    """Verify equipping an unlocked avatar works."""
    
    # 1. Perform Action (This opens its OWN session and commits)
    # Ensure we await the response properly
    response = await equip_avatar("player1", "mid")
    print(f"DEBUG: Response: {response}")
    
    if "error" in response:
        pytest.fail(f"Equip failed: {response['error']}")
        
    assert response["status"] == "ok"
    
    # 2. THE FIX: Force a fresh read
    # We clear the test session's local cache to ensure it doesn't return the old 'noob' user object
    db_session.expire_all()
    
    # 3. Query the DB directly
    # We use execute() to run a real SQL SELECT, ignoring any previous python objects
    result = await db_session.execute(select(User).where(User.id == "player1"))
    updated_user = result.scalar_one()
    
    assert updated_user.current_avatar_id == "mid"

async def test_equip_locked_fails(db_session, avatar_setup):
    """Verify you cannot equip a locked avatar via API."""
    response = await equip_avatar("player1", "pro") # Requires Lvl 10
    
    assert "error" in response
    assert "Level 10 required" in response["error"]
    
    # Verify DB did NOT update
    db_session.expire_all()
    result = await db_session.execute(select(User).where(User.id == "player1"))
    user = result.scalar_one()
    
    assert user.current_avatar_id == "noob"

import pytest
from datetime import datetime, timedelta
from sqlmodel import select
from arcade_app.models import BossDefinition, BossEncounter, User, Profile
from arcade_app.boss_helper import create_encounter, get_active_encounter, resolve_boss_attempt
import pytest_asyncio
import uuid

@pytest_asyncio.fixture
async def user_factory(db_session):
    async def _create_user(user_id=None):
        uid = user_id or f"user_{uuid.uuid4().hex[:8]}"
        user = User(id=uid, name="Test User")
        db_session.add(user)
        # Create profile too
        profile = Profile(user_id=uid, integrity=100)
        db_session.add(profile)
        await db_session.commit()
        return user
    return _create_user

@pytest_asyncio.fixture
async def boss_factory(db_session):
    async def _create_boss(**kwargs):
        bid = kwargs.get("id", f"boss_{uuid.uuid4().hex[:8]}")
        defaults = {
            "id": bid,
            "world_id": "world-python",
            "title": "Test Boss",
            "slugline": "A test boss",
            "technical_objective": "Do something",
            "starting_code": "# Test code",
            "rubric": "Test rubric",
            "pass_threshold": 70,
            "xp_reward": 500,
            "integrity_damage": 20
        }
        defaults.update(kwargs)
        boss = BossDefinition(**defaults)
        db_session.add(boss)
        await db_session.commit()
        return boss
    return _create_boss

@pytest.mark.asyncio
async def test_create_boss_encounter_only_one_active(db_session, user_factory, boss_factory):
    user = await user_factory()
    boss = await boss_factory()
    
    # Create first encounter
    enc1 = await create_encounter(user.id, boss.id)
    assert enc1.status == "active"
    assert enc1.boss_id == boss.id
    
    # Try to create another one - should return the existing one
    enc2 = await create_encounter(user.id, boss.id)
    assert enc1.id == enc2.id
    assert enc2.status == "active"

@pytest.mark.asyncio
async def test_get_active_encounter_expires(db_session, user_factory, boss_factory):
    user = await user_factory()
    boss = await boss_factory()
    
    # Create an encounter that expired in the past
    enc = BossEncounter(
        user_id=user.id,
        boss_id=boss.id,
        status="active",
        started_at=datetime.utcnow() - timedelta(hours=1),
        expires_at=datetime.utcnow() - timedelta(minutes=1)
    )
    db_session.add(enc)
    await db_session.commit()
    
    # Fetching it should mark it as expired and return None
    active = await get_active_encounter(user.id)
    assert active is None
    
    await db_session.refresh(enc)
    assert enc.status == "expired"

@pytest.mark.asyncio
async def test_resolve_boss_attempt_success(db_session, user_factory, boss_factory):
    user = await user_factory()
    boss = await boss_factory(pass_threshold=70, xp_reward=500)
    
    enc = await create_encounter(user.id, boss.id)
    
    # Submit a passing score
    enc, status = await resolve_boss_attempt(user.id, enc.id, 80)
    
    assert status == "success"
    assert enc.status == "success"
    
    # Check XP reward
    stmt = select(Profile).where(Profile.user_id == user.id)
    result = await db_session.execute(stmt)
    profile = result.scalars().first()
    
    assert profile.total_xp >= 500

@pytest.mark.asyncio
async def test_resolve_boss_attempt_failure(db_session, user_factory, boss_factory):
    user = await user_factory()
    boss = await boss_factory(pass_threshold=70, integrity_damage=20)
    
    enc = await create_encounter(user.id, boss.id)
    
    # Submit a failing score
    enc, status = await resolve_boss_attempt(user.id, enc.id, 40)
    
    assert status == "failed"
    assert enc.status == "failed"
    
    # Check Integrity damage
    stmt = select(Profile).where(Profile.user_id == user.id)
    result = await db_session.execute(stmt)
    profile = result.scalars().first()
    assert profile.integrity == 80 # 100 - 20

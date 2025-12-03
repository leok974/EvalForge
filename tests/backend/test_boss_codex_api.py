import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from arcade_app.agent import app
from arcade_app.models import User, Profile, BossDefinition, BossCodexProgress, ProjectCodexDoc, KnowledgeChunk

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest_asyncio.fixture
async def auth_headers(db_session):
    # Setup user for auth
    user = User(id="test_user", name="Test User")
    db_session.add(user)
    await db_session.commit()
    
    profile = Profile(user_id=user.id)
    db_session.add(profile)
    await db_session.commit()
    
    # Mock auth dependency if needed, or use a real token if auth is simple.
    # Assuming "x-user-id" header or similar for dev/test auth, 
    # OR we might need to mock `get_current_user`.
    # For now, let's assume we can bypass or use a dev header if configured,
    # but based on `auth_helper.py` usually we need a token.
    # Let's try to mock the dependency override in the test itself if needed.
    return {"x-user-id": "test_user"} 

@pytest_asyncio.fixture
async def reactor_boss_def(db_session):
    boss = BossDefinition(
        id="boss-reactor-core",
        name="The Reactor Core",
        world_id="world-python",
        hint_codex_id="boss-reactor-core-strategy"
    )
    db_session.add(boss)
    await db_session.commit()
    return boss

@pytest_asyncio.fixture
async def codex_docs(db_session, reactor_boss_def):
    # Seed KnowledgeChunks for the boss
    docs = [
        ("boss-reactor-core-lore", 1, "Lore Content"),
        ("boss-reactor-core-attacks", 2, "Attacks Content"),
        ("boss-reactor-core-strategy", 3, "Strategy Content"),
    ]
    for slug, tier, content in docs:
        meta = {
            "boss_id": reactor_boss_def.id,
            "tier": tier,
            "slug": slug,
            "title": f"Title {tier}"
        }
        chunk = KnowledgeChunk(
            source_id=slug,
            source_type="codex",
            content=content,
            metadata_json=meta,
            chunk_index=0,
            embedding=[0.0]*768
        )
        db_session.add(chunk)
    await db_session.commit()

@pytest.mark.asyncio
async def test_boss_codex_starts_locked(client, db_session, auth_headers, reactor_boss_def, codex_docs):
    # Override auth dependency to force our user
    from arcade_app.auth_helper import get_current_user
    app.dependency_overrides[get_current_user] = lambda: {"id": "test_user", "name": "Test User"}

    res = await client.get(f"/api/codex/boss/{reactor_boss_def.id}", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()

    assert data["boss"]["tier_unlocked"] == 0
    tiers = {doc["tier"]: doc for doc in data["docs"]}

    # Tier 1 should be locked (or unlocked if logic says tier 0 is locked)
    # Based on user spec: Tier 1 unlocks on first encounter/death. So initially locked.
    assert tiers[1]["unlocked"] is False
    assert tiers[1]["body_md"] is None
    assert tiers[3]["unlocked"] is False

    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_boss_codex_respects_progress(client, db_session, auth_headers, reactor_boss_def, codex_docs):
    from arcade_app.auth_helper import get_current_user
    app.dependency_overrides[get_current_user] = lambda: {"id": "test_user", "name": "Test User"}
    
    # Get profile
    from sqlmodel import select
    profile = (await db_session.exec(select(Profile).where(Profile.user_id == "test_user"))).first()

    # Manually bump progress to Tier 2
    progress = BossCodexProgress(
        profile_id=profile.id, 
        boss_id=reactor_boss_def.id, 
        tier_unlocked=2
    )
    db_session.add(progress)
    await db_session.commit()

    res = await client.get(f"/api/codex/boss/{reactor_boss_def.id}", headers=auth_headers)
    data = res.json()
    tiers = {doc["tier"]: doc for doc in data["docs"]}

    assert tiers[1]["unlocked"] is True
    assert tiers[1]["body_md"] == "Lore Content"
    assert tiers[2]["unlocked"] is True
    assert tiers[2]["body_md"] == "Attacks Content"
    assert tiers[3]["unlocked"] is False
    assert tiers[3]["body_md"] is None

    app.dependency_overrides = {}

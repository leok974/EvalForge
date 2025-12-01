"""Test boss history API endpoint."""
import pytest
from datetime import datetime, UTC

from arcade_app.models import BossDefinition, BossRun


@pytest.mark.anyio
async def test_boss_history_returns_recent_runs(async_client, test_db_session, auth_headers):
    """Test that /api/boss/history returns ordered boss runs."""
    # Seed one boss
    boss = BossDefinition(
        id="reactor_core",
        world_id="world-python",
        track_id=None,
        title="Reactor Core Meltdown",
        slugline="Contain the breach",
        technical_objective="Fix async reactor",
        starting_code="# code",
        rubric="# rubric",
        time_limit_seconds=1800,
        pass_threshold=70,
        xp_reward=300,
        integrity_damage=10,
        difficulty="normal",
    )
    test_db_session.add(boss)
    await test_db_session.commit()

    # Create two runs
    r1 = BossRun(
        user_id="leo",
        boss_id="reactor_core",
        difficulty="normal",
        score=60,
        passed=False,
        integrity_delta=-10,
        xp_awarded=0,
        created_at=datetime(2025, 1, 1, 10, 0, 0, tzinfo=UTC),
    )
    r2 = BossRun(
        user_id="leo",
        boss_id="reactor_core",
        difficulty="hard",
        score=90,
        passed=True,
        integrity_delta=20,
        xp_awarded=600,
        created_at=datetime(2025, 1, 2, 10, 0, 0, tzinfo=UTC),
    )
    test_db_session.add(r1)
    test_db_session.add(r2)
    await test_db_session.commit()

    resp = await async_client.get("/api/boss/history?limit=5", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2

    # Should be ordered newest → oldest
    assert data[0]["score"] == 90
    assert data[0]["passed"] is True
    assert data[0]["difficulty"] == "hard"
    assert data[1]["score"] == 60
    assert data[1]["passed"] is False
    assert data[1]["difficulty"] == "normal"


@pytest.mark.anyio
async def test_boss_history_requires_auth(async_client):
    """Test that /api/boss/history requires authentication."""
    resp = await async_client.get("/api/boss/history")
    assert resp.status_code == 401


@pytest.mark.anyio
async def test_boss_history_empty_when_no_runs(async_client, auth_headers):
    """Test that /api/boss/history returns empty list when user has no runs."""
    resp = await async_client.get("/api/boss/history?limit=5", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data == []

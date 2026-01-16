import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlmodel import select
# Import app to use in AsyncClient
from arcade_app.agent import app
from arcade_app.progress_models import QuestProgressV2, QuestHintUnlock

# Mark all as async
pytestmark = pytest.mark.asyncio

async def test_run_quest_python(client, db_session):
    # 1. Run correct code
    payload = {
        "code": "def main():\n    for i in range(3):\n        print('liftoff')\n",
        "language": "python",
        "mode": "validate"
    }
    # Mock auth header
    headers = {"X-Dev-User": "test-user-1"}
    
    resp = await client.post("/api/quests/foundry-ignition/run", json=payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["passed"] == True
    assert data["ready_to_submit"] == True
    
    # 2. Check DB side effects
    # Progress should be created
    q = await db_session.execute(select(QuestProgressV2).where(QuestProgressV2.user_id == "test-user-1"))
    row = q.scalar_one()
    assert row.quest_id == "foundry-ignition"
    assert row.runs_count == 1
    assert row.status == "in_progress"

async def test_submit_quest_success(client, db_session):
    payload = {
        "code": "def main():\n    for i in range(3):\n        print('liftoff')\n",
        "language": "python"
    }
    headers = {"X-Dev-User": "test-user-2"}
    
    resp = await client.post("/api/quests/foundry-ignition/submit", json=payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] == True
    assert data["status"] == "completed"
    assert data["xp_awarded"] == 50
    
    # DB Check
    q = await db_session.execute(select(QuestProgressV2).where(QuestProgressV2.user_id == "test-user-2"))
    row = q.scalar_one()
    assert row.status == "completed"
    assert row.attempts_count == 1 # Submit counts as attempt

async def test_unlock_hints_flow(client, db_session):
    headers = {"X-Dev-User": "test-user-3"}
    quest_id = "foundry-ignition"
    
    # 1. Try to unlock tier 1 without running -> Should fail or succeed? 
    # Logic: require >= tier runs. 0 runs < 1.
    resp = await client.post(f"/api/quests/{quest_id}/hints/unlock?tier=1", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["ok"] == False
    
    # 2. Run once
    payload = {"code": "print('fail')", "language": "python"}
    await client.post(f"/api/quests/{quest_id}/run", json=payload, headers=headers)
    
    # 3. Unlock tier 1 -> Success
    resp = await client.post(f"/api/quests/{quest_id}/hints/unlock?tier=1", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["ok"] == True
    assert resp.json()["max_tier"] == 1
    
    # 4. Check DB
    q = await db_session.execute(select(QuestHintUnlock).where(QuestHintUnlock.user_id == "test-user-3"))
    row = q.scalar_one()
    assert row.max_tier == 1

import pytest
import httpx
import os
from typing import Dict, Any

BASE_URL = os.getenv("EVALFORGE_BASE_URL", "http://localhost:8092")

@pytest.mark.asyncio
async def test_sql_select_objectives_regression():
    """
    Verify that sql-select has the correct objectives and NO fs_snapshot or obj_join.
    """
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=60) as client:
        # Run sql-select
        payload = {
            "mode": "execute",
            "language": "sql",
            "code": "SELECT name, city FROM users ORDER BY name ASC;",
            "idempotency_key": f"test-sql-select-{os.urandom(4).hex()}"
        }
        
        headers = {"X-Dev-User": "test-user"}
        response = await client.post("/api/quests/sql-select/run", json=payload, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # 1. Ensure no fs_snapshot or obj_join
        objective_ids = [obj["id"] for obj in data["objective_results"]]
        assert "fs_snapshot" not in objective_ids, "sql-select should NOT have fs_snapshot objective"
        assert "obj_join" not in objective_ids, "sql-select should NOT have obj_join objective (it's not a join quest)"
        
        # 2. Ensure obj_syntax is present (as added in our fix)
        assert "obj_syntax" in objective_ids
        
        # 3. Double check artifacts for rendering
        assert "artifacts" in data
        assert "sql_student_result" in data["artifacts"]
        result = data["artifacts"]["sql_student_result"]
        assert "columns" in result
        assert "rows" in result
        assert len(result["rows"]) == 6

@pytest.mark.asyncio
async def test_sql_where_objectives_regression():
    """
    Verify that sql-where has NO fs_snapshot.
    """
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=60) as client:
        # Run sql-where
        payload = {
            "mode": "execute",
            "language": "sql",
            "code": "SELECT id, name, age FROM users WHERE is_active = 1 AND city = 'Detroit' AND age >= 25 ORDER BY id ASC;",
            "idempotency_key": f"test-sql-where-{os.urandom(4).hex()}"
        }
        
        headers = {"X-Dev-User": "test-user"}
        response = await client.post("/api/quests/sql-where/run", json=payload, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        objective_ids = [obj["id"] for obj in data["objective_results"]]
        assert "fs_snapshot" not in objective_ids, "sql-where should NOT have fs_snapshot objective"
        assert "obj_runs" in objective_ids
        assert "obj_syntax" in objective_ids

@pytest.mark.asyncio
async def test_sql_preview_logging_redirection():
    """
    Verify that INFO logs from sql_preview go to stdout (not triggering Runtime Error in UI).
    While we can't easily check stdout of the runner from the API, 
    we can check that the stderr in the response doesn't contain INFO[sql-preview].
    """
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=60) as client:
        payload = {
            "mode": "execute",
            "language": "sql",
            "code": "SELECT 1;",
            "idempotency_key": f"test-sql-log-{os.urandom(4).hex()}"
        }
        
        headers = {"X-Dev-User": "test-user"}
        response = await client.post("/api/quests/sql-ignition/run", json=payload, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # If redirect worked, INFO[sql-preview] should NOT be in stderr
        # (It would be in stdout, but the API response returns sanitized stderr)
        stderr = data.get("stderr", "")
        assert "INFO[sql-preview]" not in stderr, "INFO logs should NOT be in stderr (they trigger the Error banner in UI)"

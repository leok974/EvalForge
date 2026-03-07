import pytest
import pytest_asyncio
import os
from httpx import AsyncClient
from arcade_app.models import QuestDefinition
from arcade_app.progress_models import QuestProgressV2
from arcade_app.database import get_session
from sqlmodel import select

@pytest_asyncio.fixture
async def seed_sql_quest(db_session):
    """Seed the sql-select quest for smoke testing."""
    quest = QuestDefinition(
        slug="sql-select",
        world_id="sql",
        track_id="basics",
        order_index=1,
        title="SQL Select Basics",
        short_description="Learn to select columns.",
        detailed_description="Use SELECT to find names and cities.",
        language="sql",
        workspace_json={
            "files": [
                {"path": "task.sql", "content": "SELECT name, city FROM users;", "editable": True},
                {"path": "fixtures/schema.sql", "content": "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, city TEXT);", "editable": False},
                {"path": "fixtures/seed.sql", "content": "INSERT INTO users (name, city) VALUES ('Alice', 'Detroit'), ('Bob', 'NYC'), ('Charlie', 'LA'), ('David', 'SF'), ('Eve', 'Chicago'), ('Frank', 'Miami');", "editable": False},
            ],
            "entrypoint": "task.sql"
        }
    )
    db_session.add(quest)
    await db_session.commit()
    await db_session.refresh(quest)
    return quest

@pytest.mark.asyncio
async def test_sql_preview_artifacts(client, seed_sql_quest, monkeypatch):
    """
    Assert that hitting the run endpoint for a SQL quest returns 
    the expected artifacts.sql_student_result shape and data.
    """
    monkeypatch.setenv("EXECUTION_ENABLED", "1")
    
    # Mock the actual execution to avoid Docker issues in test env
    from arcade_app.services.code_runner import ExecResult
    mock_result = ExecResult(
        ok=True,
        exit_code=0,
        duration_ms=123,
        stdout="Mocked SQL output",
        stderr="",
        timed_out=False,
        artifacts={
            "sql_student_result": {
                "columns": ["name", "city"],
                "rows": [["Alice", "Detroit"], ["Bob", "NYC"]],
                "row_count": 2
            },
            "sql_trace": [{"idx": 0, "phase": "student", "sql": "SELECT...", "is_select": True}],
            "sql_explain": {"engine": "sqlite", "statement": "SELECT...", "plan_rows": ["SCAN TABLE users"]}
        }
    )
    
    with monkeypatch.context() as m:
        m.setattr("arcade_app.routers.routes_quests_runtime.run_code", lambda *args, **kwargs: mock_result)
        
        payload = {
            "code": "SELECT name, city FROM users ORDER BY name ASC;",
            "language": "sql",
            "mode": "execute",
            "workspace": [
                {"path": "task.sql", "content": "SELECT name, city FROM users ORDER BY name ASC;"}
            ]
        }
        
        headers = {"x-dev-user": "smoke-tester"}
        response = await client.post(f"/api/quests/{seed_sql_quest.slug}/run", json=payload, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    # print(f"DEBUG[test]: response_data={data}")
    
    # 1. Verify diagnostics indicate the correct runner
    # Note: runner_id is set in routes_quests_runtime based on lang and mode
    diagnostics = data.get("diagnostics", [])
    runner_diag = next((d for d in diagnostics if d.get("kind") == "runner"), None)
    assert runner_diag is not None, "Should have a runner diagnostic"
    assert runner_diag.get("runner") == "sql_preview"
    
    # 2. Verify artifacts structure
    artifacts = data.get("artifacts")
    assert artifacts is not None
    assert "sql_student_result" in artifacts
    
    res = artifacts["sql_student_result"]
    assert res["columns"] == ["name", "city"]
    assert res["row_count"] == 2
    
    # 3. Verify data (Alice is first due to our mock)
    assert res["rows"][0] == ["Alice", "Detroit"]
    
    # 4. Verify other expected artifacts
    assert "sql_trace" in artifacts
    assert "sql_explain" in artifacts
    assert artifacts["sql_explain"]["engine"] == "sqlite"

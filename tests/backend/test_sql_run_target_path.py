import pytest
import pytest_asyncio
from httpx import AsyncClient
from arcade_app.models import QuestDefinition

@pytest_asyncio.fixture
async def sql_target_quest(db_session):
    """Seed a quest with multiple SQL files for target path testing."""
    quest = QuestDefinition(
        slug="sql-target-test",
        world_id="sql",
        track_id="basics",
        order_index=99,
        title="SQL Target Test",
        short_description="Test run_target_path",
        detailed_description="Testing if we can run different files.",
        language="sql",
        workspace_json={
            "files": [
                {"path": "task.sql", "content": "SELECT 'task' as source, name, city FROM users;", "editable": True},
                {"path": "example.sql", "content": "SELECT 'example' as source, name, age FROM users;", "editable": True},
                {"path": "fixtures/schema.sql", "content": "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, city TEXT, age INTEGER);", "editable": False},
                {"path": "fixtures/seed.sql", "content": "INSERT INTO users (name, city, age) VALUES ('Alice', 'Detroit', 28);", "editable": False},
            ],
            "entrypoint": "task.sql"
        }
    )
    db_session.add(quest)
    await db_session.commit()
    await db_session.refresh(quest)
    return quest

@pytest.mark.asyncio
async def test_sql_run_target_path_selection(client, sql_target_quest, monkeypatch):
    """
    Test that run_target_path correctly selects the SQL code to run.
    """
    monkeypatch.setenv("EXECUTION_ENABLED", "1")
    
    # We don't mock run_code here because we want to test the actual logic in routes_quests_runtime
    # that resolves the code. However, the Actual runner might fail in local environment if docker isn't ready.
    # So we'll mock the runner BUT we want to see what 'code' was passed to it.
    
    captured_args = {}
    
    def mock_run_code(language, code, workspace=None, **kwargs):
        captured_args['code'] = code
        captured_args['workspace'] = workspace
        from arcade_app.services.code_runner import ExecResult
        return ExecResult(
            ok=True, exit_code=0, duration_ms=1, stdout="", stderr="", timed_out=False,
            artifacts={
                "sql_student_result": {
                    "columns": ["source", "name", "age"] if "age" in code else ["source", "name", "city"],
                    "rows": [], "row_count": 0
                }
            }
        )

    monkeypatch.setattr("arcade_app.routers.routes_quests_runtime.run_code", mock_run_code)
    
    # 1. Run example.sql
    payload = {
        "code": "", # Empty code to force workspace resolution
        "language": "sql",
        "run_target_path": "example.sql",
        "evaluate_objectives": False,
        "workspace": [] # Empty overlay
    }
    
    headers = {"x-dev-user": "test-user"}
    response = await client.post(f"/api/quests/{sql_target_quest.slug}/run", json=payload, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify the code captured by the mock wasfrom example.sql
    assert "age" in captured_args['code']
    assert "source" in captured_args['code']
    assert "example" in captured_args['code']
    
    # Verify response fields
    assert data["evaluated_objectives"] is False
    assert data["run_target_path"] == "example.sql"
    
    # Verify diagnostics
    diagnostics = data["diagnostics"]
    target_diag = next((d for d in diagnostics if d["kind"] == "sql_run_target"), None)
    assert target_diag is not None
    assert target_diag["path"] == "example.sql"

@pytest.mark.asyncio
async def test_sql_run_default_to_task(client, sql_target_quest, monkeypatch):
    """
    Test that omitting run_target_path defaults to task.sql.
    """
    monkeypatch.setenv("EXECUTION_ENABLED", "1")
    captured_args = {}
    
    def mock_run_code(language, code, workspace=None, **kwargs):
        captured_args['code'] = code
        from arcade_app.services.code_runner import ExecResult
        return ExecResult(ok=True, exit_code=0, duration_ms=1, stdout="", stderr="", timed_out=False)

    monkeypatch.setattr("arcade_app.routers.routes_quests_runtime.run_code", mock_run_code)
    
    payload = {
        "code": "",
        "language": "sql",
        "evaluate_objectives": True
    }
    
    response = await client.post(f"/api/quests/{sql_target_quest.slug}/run", json=payload, headers={"x-dev-user": "test-user"})
    assert response.status_code == 200
    
    assert "city" in captured_args['code']
    assert "task" in captured_args['code']

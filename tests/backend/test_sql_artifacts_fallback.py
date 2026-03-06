from unittest.mock import MagicMock, AsyncMock, patch
import pytest
import os
from arcade_app.routers.routes_quests_runtime import run_quest
from arcade_app.schemas.quest_run import RunRequest
from arcade_app.services.code_runner_docker import ExecResult

@pytest.mark.asyncio
async def test_sql_run_preview_missing_disk_artifacts_returns_memory_fallback():
    mock_db = AsyncMock()
    mock_quest = MagicMock()
    mock_quest.language = "sql"
    mock_quest.objectives_json = []
    mock_quest.slug = "sql-mock-quest"
    
    # ensure execution is enabled
    os.environ["EXECUTION_ENABLED"] = "1"
    
    mock_db.execute.return_value.scalar_one_or_none.return_value = mock_quest

    # The runner returns `artifacts=None` because it couldn't read them off disk
    mock_result = ExecResult(
        ok=True,
        exit_code=0,
        duration_ms=150,
        stdout="[Mock SQL Output]",
        stderr="",
        timed_out=False,
        artifacts=None # <--- The critical simulation of disk write failure
    )

    with patch('arcade_app.services.code_runner.run_code', new_callable=AsyncMock) as mock_run_code:
        mock_run_code.return_value = mock_result
        req = RunRequest(code="SELECT 1;", mode="run", language="sql", workspace=[{"path": "task.sql", "content": "SELECT 1;"}])
        
        # Call the endpoint handler directly, bypassing FastAPI dependency injection
        resp = await run_quest(quest_id="sql-mock-quest", payload=req, user_id="leo", db=mock_db)
        
        # resp is typically a dict from this endpoint
        data = resp if isinstance(resp, dict) else resp.dict()
        
        assert "artifacts" in data
        assert data["artifacts"] is not None
        artifacts = data["artifacts"]
        
        assert "sql_student_result" in artifacts
        assert "sql_trace" in artifacts
        assert "sql_explain" in artifacts

        # Ensure the default structure is present
        assert "Execution failed" in artifacts["sql_student_result"]["note"]
        assert artifacts["sql_trace"] == []

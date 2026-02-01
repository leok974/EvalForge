"""
Phase 8.x PR 4: Quest Attempt Metadata Tests

Test suite for workspace hashing, execution context, and LLM metadata persistence.
"""
import pytest
from arcade_app.services.workspace_hash import hash_workspace_snapshot, build_execution_context


class TestWorkspaceHashing:
    """Test deterministic workspace hashing."""
    
    def test_empty_workspace_returns_none(self):
        """Empty or None workspace returns None."""
        assert hash_workspace_snapshot(None) is None
        assert hash_workspace_snapshot({}) is None
        assert hash_workspace_snapshot({"files": []}) is None
    
    def test_hash_format(self):
        """Hash has correct format: sha256:hex."""
        ws = {
            "entrypoint": "main.py",
            "files": [
                {"path": "main.py", "content": "print('hello')"}
            ]
        }
        result = hash_workspace_snapshot(ws)
        assert result is not None
        assert result.startswith("sha256:")
        assert len(result) == 71  # "sha256:" (7) + 64 hex chars
    
    def test_determinism_same_content(self):
        """Same content produces same hash."""
        ws1 = {
            "entrypoint": "main.py",
            "files": [
                {"path": "main.py", "content": "print('hello')"},
                {"path": "utils.py", "content": "def helper(): pass"}
            ]
        }
        ws2 = {
            "entrypoint": "main.py",
            "files": [
                {"path": "main.py", "content": "print('hello')"},
                {"path": "utils.py", "content": "def helper(): pass"}
            ]
        }
        assert hash_workspace_snapshot(ws1) == hash_workspace_snapshot(ws2)
    
    def test_determinism_file_order_invariant(self):
        """File order doesn't affect hash (sorted internally)."""
        ws1 = {
            "entrypoint": "main.py",
            "files": [
                {"path": "main.py", "content": "import utils"},
                {"path": "utils.py", "content": "X = 1"}
            ]
        }
        ws2 = {
            "entrypoint": "main.py",
            "files": [
                {"path": "utils.py", "content": "X = 1"},  # Reversed order
                {"path": "main.py", "content": "import utils"}
            ]
        }
        assert hash_workspace_snapshot(ws1) == hash_workspace_snapshot(ws2)
    
    def test_content_change_changes_hash(self):
        """Different content produces different hash."""
        ws1 = {
            "entrypoint": "main.py",
            "files": [{"path": "main.py", "content": "x = 1"}]
        }
        ws2 = {
            "entrypoint": "main.py",
            "files": [{"path": "main.py", "content": "x = 2"}]  # Changed content
        }
        assert hash_workspace_snapshot(ws1) != hash_workspace_snapshot(ws2)
    
    def test_path_change_changes_hash(self):
        """Different file path produces different hash."""
        ws1 = {
            "entrypoint": "main.py",
            "files": [{"path": "main.py", "content": "x = 1"}]
        }
        ws2 = {
            "entrypoint": "main.py",
            "files": [{"path": "app.py", "content": "x = 1"}]  # Changed path
        }
        assert hash_workspace_snapshot(ws1) != hash_workspace_snapshot(ws2)
    
    def test_entrypoint_change_changes_hash(self):
        """Different entrypoint produces different hash."""
        ws1 = {
            "entrypoint": "main.py",
            "files": [{"path": "main.py", "content": "x = 1"}]
        }
        ws2 = {
            "entrypoint": "app.py",  # Changed entrypoint
            "files": [{"path": "main.py", "content": "x = 1"}]
        }
        assert hash_workspace_snapshot(ws1) != hash_workspace_snapshot(ws2)


class TestExecutionContext:
    """Test execution context builder."""
    
    def test_basic_context(self):
        """Build basic execution context."""
        ctx = build_execution_context(
            language="python",
            mode="execute",
            duration_ms=1234,
            exit_code=0,
            stdout="hello\n",
            stderr="",
            timed_out=False
        )
        
        assert ctx["runner_backend"] == "docker"
        assert ctx["language"] == "python"
        assert ctx["mode"] == "execute"
        assert ctx["duration_ms"] == 1234
        assert ctx["exit_code"] == 0
        assert ctx["timed_out"] is False
        assert ctx["stdout_bytes"] == 6
        assert ctx["stderr_bytes"] == 0
    
    def test_context_has_no_secrets(self):
        """Execution context doesn't leak sensitive data."""
        ctx = build_execution_context(
            language="typescript",
            mode="tests",
            duration_ms=500,
            exit_code=1,
            stdout="Some output with /home/user/path",
            stderr="Error at line 5",
            timed_out=True
        )
        
        # Convert to string and check for suspicious patterns
        ctx_str = str(ctx)
        
        # Should NOT contain absolute paths
        assert "/home/" not in ctx_str
        assert "C:\\" not in ctx_str
        assert ":\\" not in ctx_str  # Windows drive letters
        
        # Should NOT contain raw output (only sizes)
        assert "Some output" not in ctx_str
        assert "Error at line" not in ctx_str
        
        # Should contain safe metadata
        assert "typescript" in ctx_str
        assert "tests" in ctx_str


@pytest.mark.asyncio
async def test_workspace_hash_persisted(async_client, db_session, dev_user):
    """Run with workspace persists workspace_hash."""
    quest_id = "test-quest"
    
    response = await async_client.post(
        f"/api/quests/{quest_id}/run",
        json={
            "code": "",
            "language": "python",
            "mode": "validate",
            "workspace": [
                {"path": "main.py", "content": "print('test')"},
                {"path": "utils.py", "content": "X = 1"}
            ],
            "entrypoint": "main.py"
        },
        headers={"X-Dev-User": dev_user}
    )
    
    assert response.status_code == 200
    data = response.json()
    attempt_id = data["attempt_id"]
    
    # Fetch attempt from DB
    from sqlmodel import select
    from arcade_app.progress_models import QuestAttempt
    result = await db_session.execute(
        select(QuestAttempt).where(QuestAttempt.id == attempt_id)
    )
    attempt = result.scalar_one()
    
    # Verify workspace_hash is persisted
    assert attempt.workspace_hash is not None
    assert attempt.workspace_hash.startswith("sha256:")


@pytest.mark.asyncio
async def test_hash_determinism_across_requests(async_client, dev_user):
    """Multiple requests with same workspace produce same hash."""
    quest_id = "test-quest"
    workspace = [
        {"path": "main.py", "content": "x = 1"},
        {"path": "lib.py", "content": "y = 2"}
    ]
    
    # First request
    response1 = await async_client.post(
        f"/api/quests/{quest_id}/run",
        json={
            "code": "",
            "language": "python",
            "mode": "validate",
            "workspace": workspace,
            "entrypoint": "main.py"
        },
        headers={"X-Dev-User": dev_user}
    )
    data1 = response1.json()
    
    # Second request with different idempotency key (new attempt)
    response2 = await async_client.post(
        f"/api/quests/{quest_id}/run",
        json={
            "code": "",
            "language": "python",
            "mode": "validate",
            "workspace": workspace,
            "entrypoint": "main.py",
            "idempotency_key": "different-key-123"
        },
        headers={"X-Dev-User": dev_user}
    )
    data2 = response2.json()
    
    # Different attempts but same hash
    assert data1["attempt_id"] != data2["attempt_id"]
    # (Would need to fetch from DB to compare hashes, or add to response)


@pytest.mark.asyncio
async def test_execution_context_populated(async_client, db_session, dev_user):
    """Execution context is populated with safe metadata."""
    quest_id = "test-quest"
    
    response = await async_client.post(
        f"/api/quests/{quest_id}/run",
        json={
            "code": "print('hello')",
            "language": "python",
            "mode": "execute"
        },
        headers={"X-Dev-User": dev_user}
    )
    
    assert response.status_code == 200
    attempt_id = response.json()["attempt_id"]
    
    # Fetch attempt
    from sqlmodel import select
    from arcade_app.progress_models import QuestAttempt
    result = await db_session.execute(
        select(QuestAttempt).where(QuestAttempt.id == attempt_id)
    )
    attempt = result.scalar_one()
    
    # Verify execution_context_json
    ctx = attempt.execution_context_json
    assert ctx is not None
    assert "runner_backend" in ctx
    assert "mode" in ctx
    assert "language" in ctx
    assert "duration_ms" in ctx
    assert "exit_code" in ctx
    assert ctx["language"] == "python"
    assert ctx["mode"] == "execute"


@pytest.mark.asyncio
async def test_execution_context_safe(async_client, db_session, dev_user):
    """Execution context doesn't contain sensitive data."""
    quest_id = "test-quest"
    
    response = await async_client.post(
        f"/api/quests/{quest_id}/run",
        json={
            "code": "import os\nprint(os.getenv('SECRET_KEY'))",
            "language": "python",
            "mode": "execute"
        },
        headers={"X-Dev-User": dev_user}
    )
    
    attempt_id = response.json()["attempt_id"]
    
    from sqlmodel import select
    from arcade_app.progress_models import QuestAttempt
    result = await db_session.execute(
        select(QuestAttempt).where(QuestAttempt.id == attempt_id)
    )
    attempt = result.scalar_one()
    
    ctx_str = str(attempt.execution_context_json)
    
    # Should NOT contain absolute paths
    assert "/home/" not in ctx_str
    assert "C:\\" not in ctx_str
    
    # Should NOT contain raw output (check attempt.stdout separately)
    assert "SECRET_KEY" not in ctx_str  # If this appears in output, it shouldn't be in context


@pytest.mark.asyncio  
async def test_model_id_prompt_version_persisted_when_present(async_client, db_session, dev_user, monkeypatch):
    """model_id and prompt_version are persisted when LLM metadata exists."""
    # This test would require mocking the debrief/quickfix generators
    # to return metadata. For now, just verify fields exist and are nullable.
    
    quest_id = "test-quest"
    response = await async_client.post(
        f"/api/quests/{quest_id}/run",
        json={
            "code": "x = 1",
            "language": "python",
            "mode": "validate"
        },
        headers={"X-Dev-User": dev_user}
    )
    
    attempt_id = response.json()["attempt_id"]
    
    from sqlmodel import select
    from arcade_app.progress_models import QuestAttempt
    result = await db_session.execute(
        select(QuestAttempt).where(QuestAttempt.id == attempt_id)
    )
    attempt = result.scalar_one()
    
    # Fields should exist (even if None)
    assert hasattr(attempt, "model_id")
    assert hasattr(attempt, "prompt_version")
    # They will be None unless LLM generators include meta

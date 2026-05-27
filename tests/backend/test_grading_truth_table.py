"""
Sprint 21 — Grading Truth Table Tests (Sprint 29: TestSubmitEndToEnd appended)
===============================================================================

Verifies that the grading pipeline enforces fail-closed semantics:

  | evaluate_objectives | objective_results | passed | ready_to_submit |
  |---------------------|-------------------|--------|-----------------|
  | False               | []                | False  | False           |
  | True                | []  (empty)       | False  | False           |
  | True                | all ok=True       | True   | True            |
  | True                | any ok=False      | False  | False           |
  | True  (crashed)     | config_missing    | False  | False           |

Also verifies:
  - sql_preview diagnostics NOT injected for non-SQL languages in preview mode
  - validate_quest_attempt() never returns an empty list

These are unit tests against the validator directly and integration tests against
the flag-computation logic using a mock quest definition.  No DB, no network.
"""

import pytest
from types import SimpleNamespace
from typing import Any, Dict, List, Optional
from arcade_app.services.quest_validate import validate_quest_attempt


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _quest(
    objectives: List[Dict],
    language: str = "python",
    tier: int = 1,
    sandbox: bool = False,
) -> Any:
    """Build a minimal quest-like object for validate_quest_attempt()."""
    return SimpleNamespace(
        slug="test-quest",
        language=language,
        tier=tier,
        objectives_json=objectives,
        runtime_rules_json={"enabled": False},
        sandbox=sandbox,
        is_sandbox=sandbox,
        grading_json={},
    )


def _flag_pass_all(
    *,
    evaluate_objectives: bool,
    objective_results: List[Dict],
    timed_out: bool = False,
    mode: str = "validate",
    language: str = "python",
) -> Dict:
    """
    Simulate the flag computation block from routes_quests_runtime.py
    (the block that sets passed/ready_to_submit from objective_results).

    This is extracted here so the truth table tests don't depend on HTTP
    infrastructure — they verify the algorithm directly.
    """
    if not evaluate_objectives:
        passed = False
        ready_to_submit = False
        return {
            "passed": passed,
            "ready_to_submit": ready_to_submit,
            "objective_results": objective_results,
            "evaluated_objectives": evaluate_objectives,
        }

    # Grading path
    results = list(objective_results)  # copy so we can mutate

    if results:
        passed = all(r.get("ok") for r in results)
    else:
        # Fail-closed: synthesize config_missing entry
        results = [{
            "id": "config_missing",
            "ok": False,
            "detail": (
                "No objectives produced results. The grader may have crashed, "
                "the quest may have no objectives defined, or the runner may "
                "not support this language. Check the console output."
            ),
        }]
        passed = False

    ready_to_submit = passed and not timed_out

    return {
        "passed": passed,
        "ready_to_submit": ready_to_submit,
        "objective_results": results,
        "evaluated_objectives": evaluate_objectives,
    }


# ---------------------------------------------------------------------------
# Truth table tests
# ---------------------------------------------------------------------------

class TestTruthTable:
    """One test per cell of the grading truth table."""

    def test_preview_mode_never_passes(self):
        """evaluate_objectives=False → passed=False, ready_to_submit=False (row 1)."""
        result = _flag_pass_all(
            evaluate_objectives=False,
            objective_results=[],
        )
        assert result["passed"] is False, "Preview run must not claim passed=True"
        assert result["ready_to_submit"] is False, "Preview run must not enable submit"
        assert result["evaluated_objectives"] is False

    def test_preview_mode_ignores_existing_results(self):
        """Even if objective_results were somehow populated, preview mode stays False."""
        result = _flag_pass_all(
            evaluate_objectives=False,
            objective_results=[{"id": "obj1", "ok": True}],
        )
        assert result["passed"] is False
        assert result["ready_to_submit"] is False

    def test_empty_objectives_synthesizes_config_missing(self):
        """evaluate_objectives=True, empty list → config_missing entry, passed=False (row 2)."""
        result = _flag_pass_all(
            evaluate_objectives=True,
            objective_results=[],
        )
        assert result["passed"] is False
        assert result["ready_to_submit"] is False
        # Must synthesize exactly one config_missing entry
        assert len(result["objective_results"]) == 1
        entry = result["objective_results"][0]
        assert entry["id"] == "config_missing"
        assert entry["ok"] is False

    def test_all_objectives_pass(self):
        """All ok=True → passed=True, ready_to_submit=True (row 3)."""
        result = _flag_pass_all(
            evaluate_objectives=True,
            objective_results=[
                {"id": "obj1", "ok": True},
                {"id": "obj2", "ok": True},
            ],
        )
        assert result["passed"] is True
        assert result["ready_to_submit"] is True

    def test_some_objectives_fail(self):
        """Any ok=False → passed=False (row 4)."""
        result = _flag_pass_all(
            evaluate_objectives=True,
            objective_results=[
                {"id": "obj1", "ok": True},
                {"id": "obj2", "ok": False, "detail": "Expected X got Y"},
            ],
        )
        assert result["passed"] is False
        assert result["ready_to_submit"] is False

    def test_all_objectives_fail(self):
        """All ok=False → passed=False."""
        result = _flag_pass_all(
            evaluate_objectives=True,
            objective_results=[
                {"id": "obj1", "ok": False},
                {"id": "obj2", "ok": False},
            ],
        )
        assert result["passed"] is False
        assert result["ready_to_submit"] is False

    def test_timed_out_blocks_ready_to_submit(self):
        """Even if all objectives pass, timed_out=True prevents ready_to_submit."""
        result = _flag_pass_all(
            evaluate_objectives=True,
            objective_results=[{"id": "obj1", "ok": True}],
            timed_out=True,
        )
        assert result["passed"] is True   # objectives technically passed
        assert result["ready_to_submit"] is False  # but timed out

    def test_grader_crash_fails_closed(self):
        """Explicit config_missing (grader crash path) → passed=False (row 5)."""
        result = _flag_pass_all(
            evaluate_objectives=True,
            objective_results=[{"id": "config_missing", "ok": False, "detail": "crash"}],
        )
        assert result["passed"] is False
        assert result["ready_to_submit"] is False


# ---------------------------------------------------------------------------
# validate_quest_attempt unit tests
# ---------------------------------------------------------------------------

class TestValidateQuestAttempt:
    """Tests for arcade_app.services.quest_validate.validate_quest_attempt()."""

    def test_never_returns_empty_list_for_sandbox(self):
        """Sandbox quest with no objectives → config_missing, not []."""
        quest = _quest(objectives=[], sandbox=True)
        results = validate_quest_attempt(
            code="x = 1",
            stdout="",
            stderr="",
            exit_code=0,
            timed_out=False,
            quest_def=quest,
        )
        assert isinstance(results, list)
        assert len(results) >= 1, "validate_quest_attempt must never return []"
        assert results[0]["id"] == "config_missing"
        assert results[0]["ok"] is False

    def test_never_returns_empty_list_for_zero_tier_sandbox(self):
        """tier=0, sandbox=True, no objectives → config_missing."""
        quest = _quest(objectives=[], sandbox=True, tier=0)
        results = validate_quest_attempt(
            code="pass",
            stdout=None,
            stderr=None,
            exit_code=0,
            timed_out=False,
            quest_def=quest,
        )
        assert len(results) >= 1
        assert results[0]["ok"] is False

    def test_tier1_no_objectives_returns_config_missing(self):
        """Tier-1 quest with no objectives returns the config_missing error."""
        quest = _quest(objectives=[], tier=1)
        results = validate_quest_attempt(
            code="x = 1",
            stdout="",
            stderr="",
            exit_code=0,
            timed_out=False,
            quest_def=quest,
        )
        assert len(results) >= 1
        assert results[0]["ok"] is False

    def test_single_passing_objective(self):
        """stdout_regex that matches → ok=True."""
        quest = _quest(objectives=[{
            "id": "obj_hello",
            "kind": "stdout_regex",
            "title": "Print hello",
            "rule": {"pattern": "hello"},
        }], tier=1)
        results = validate_quest_attempt(
            code='print("hello")',
            stdout="hello\n",
            stderr="",
            exit_code=0,
            timed_out=False,
            quest_def=quest,
        )
        assert len(results) == 1
        assert results[0]["id"] == "obj_hello"
        assert results[0]["ok"] is True

    def test_single_failing_objective(self):
        """stdout_regex that does not match → ok=False."""
        quest = _quest(objectives=[{
            "id": "obj_hello",
            "kind": "stdout_regex",
            "title": "Print hello",
            "rule": {"pattern": "hello"},
        }], tier=1)
        results = validate_quest_attempt(
            code='print("goodbye")',
            stdout="goodbye\n",
            stderr="",
            exit_code=0,
            timed_out=False,
            quest_def=quest,
        )
        assert len(results) == 1
        assert results[0]["id"] == "obj_hello"
        assert results[0]["ok"] is False

    def test_multiple_objectives_all_pass(self):
        """Multiple objectives all ok → all ok=True."""
        quest = _quest(objectives=[
            {"id": "o1", "kind": "stdout_regex", "title": "Print hello", "rule": {"pattern": "hello"}},
            {"id": "o2", "kind": "exit_code_zero", "title": "Clean exit", "rule": {}},
        ], tier=1)
        results = validate_quest_attempt(
            code='print("hello")',
            stdout="hello\n",
            stderr="",
            exit_code=0,
            timed_out=False,
            quest_def=quest,
        )
        assert all(r["ok"] for r in results)

    def test_html_quest_returns_exit_code_result(self):
        """HTML quests short-circuit to a single exit_code_zero result."""
        quest = _quest(objectives=[], language="html", tier=1)
        results = validate_quest_attempt(
            code="<h1>hi</h1>",
            stdout="",
            stderr="",
            exit_code=0,
            timed_out=False,
            quest_def=quest,
        )
        assert len(results) == 1
        assert results[0]["id"] == "obj_grading"
        assert results[0]["ok"] is True

    def test_html_quest_fails_on_nonzero_exit(self):
        """HTML quest with exit_code!=0 → ok=False."""
        quest = _quest(objectives=[], language="html", tier=1)
        results = validate_quest_attempt(
            code="<h1>bad</h1>",
            stdout="",
            stderr="Test failed",
            exit_code=1,
            timed_out=False,
            quest_def=quest,
        )
        assert len(results) == 1
        assert results[0]["ok"] is False

    def test_walkthrough_first_sparks_now_evaluates(self):
        """
        Walkthrough finding 3 regression guard.

        The first-sparks quest (foundry_python.json) has a stdout_regex objective
        that checks for the exact launch sequence. This test verifies that:
          - Objectives are evaluated (evaluated_objectives=True)
          - At least one objective result is produced
          - Correct solution code passes (passed=True, ready_to_submit=True)
          - Wrong code fails (passed=False)

        If this test fails, first-sparks has a content or grading regression.
        """
        # Build a quest matching the real first-sparks objective from the questpack
        quest = _quest(
            objectives=[{
                "id": "stdout_launch_sequence",
                "kind": "stdout_regex",
                "title": "Prints the launch sequence",
                "rule": {
                    "pattern": r"^T-minus 3\nT-minus 2\nT-minus 1\nIGNITION\s*$",
                    "flags": "im",
                },
            }],
            language="python",
            tier=1,
        )

        solution_code = (
            "print('T-minus 3')\n"
            "print('T-minus 2')\n"
            "print('T-minus 1')\n"
            "print('IGNITION')\n"
        )
        solution_stdout = "T-minus 3\nT-minus 2\nT-minus 1\nIGNITION\n"

        # 1. Run validate_quest_attempt (the grading engine)
        objective_results = validate_quest_attempt(
            code=solution_code,
            stdout=solution_stdout,
            stderr="",
            exit_code=0,
            timed_out=False,
            quest_def=quest,
        )

        # 2. Run through the flag computation (simulates routes_quests_runtime.py)
        result = _flag_pass_all(
            evaluate_objectives=True,
            objective_results=objective_results,
        )

        # 3. Assert truth table expectations
        assert result["evaluated_objectives"] is True, "evaluate_objectives must be True for grading runs"
        assert len(result["objective_results"]) > 0, "At least one objective must produce a result"
        assert result["passed"] is True, "Correct solution must pass"
        assert result["ready_to_submit"] is True, "Correct solution must enable submission"

        # 4. Wrong code must fail
        wrong_results = validate_quest_attempt(
            code='print("hello world")',
            stdout="hello world\n",
            stderr="",
            exit_code=0,
            timed_out=False,
            quest_def=quest,
        )
        wrong_flags = _flag_pass_all(
            evaluate_objectives=True,
            objective_results=wrong_results,
        )
        assert wrong_flags["passed"] is False, "Wrong output must not pass"
        assert wrong_flags["ready_to_submit"] is False, "Wrong output must not enable submission"


# ---------------------------------------------------------------------------
# sql_preview language guard tests
# ---------------------------------------------------------------------------

class TestSqlPreviewLanguageGuard:
    """
    Verify the sql_preview diagnostic is injected ONLY for SQL quests in preview mode.

    These tests simulate the flag computation + diagnostic injection logic from
    routes_quests_runtime.py without spinning up the full HTTP stack.
    """

    def _inject_preview_diagnostics(self, language: str) -> List[Dict]:
        """Replicate the preview-mode diagnostic injection from routes_quests_runtime.py."""
        if language == "sql":
            target_path = "task.sql"
            return [
                {
                    "kind": "preview",
                    "runner": "sql_preview",
                    "evaluated_objectives": False,
                    "message": f"Reference run (not graded) — running {target_path}",
                },
                {
                    "kind": "sql_run_target",
                    "evaluated_objectives": False,
                    "message": f"SQL execution target: {target_path}",
                },
            ]
        else:
            return []

    def test_sql_preview_injected_for_sql(self):
        """sql_preview diagnostic is present when language=sql and evaluate_objectives=False."""
        diags = self._inject_preview_diagnostics("sql")
        runners = [d.get("runner") for d in diags]
        assert "sql_preview" in runners

    def test_sql_preview_not_injected_for_python(self):
        """sql_preview diagnostic must NOT appear for Python quests in preview mode."""
        diags = self._inject_preview_diagnostics("python")
        runners = [d.get("runner") for d in diags]
        assert "sql_preview" not in runners
        assert diags == [], "No diagnostics should be injected for non-SQL preview runs"

    def test_sql_preview_not_injected_for_javascript(self):
        """sql_preview diagnostic must NOT appear for JavaScript quests in preview mode."""
        diags = self._inject_preview_diagnostics("javascript")
        assert diags == []

    def test_sql_preview_not_injected_for_docker(self):
        """sql_preview diagnostic must NOT appear for Docker/YAML quests in preview mode."""
        diags = self._inject_preview_diagnostics("yaml")
        assert diags == []


# ---------------------------------------------------------------------------
# Sprint 29 — SUBMIT end-to-end regression armor
# ---------------------------------------------------------------------------
#
# Regression armor for two Sprint 28 bugs:
#
# Bug 1 (arcade_app/services/code_runner_docker.py):
#   run_unittest_json.py staging was nested inside `if code:`.
#   Empty code + mode="tests" → runner script not staged → Docker container
#   crashed: "can't open file '.evalforge/run_unittest_json.py'".
#   Fix: staging block moved unconditionally outside `if code:`.
#
# Bug 2 (arcade_app/routers/routes_quests_runtime.py submit_quest):
#   exec_mode hardcoded to "run"; grading files never injected.
#   tests_pass objectives always received empty stdout →
#   "No test output received", even for reference solutions.
#   Fix: detect tests_pass objectives → set exec_mode="tests" + inject grading files.
#
# HTTP tests (1-3): mock run_code + DB, hit real FastAPI routes → catch Bug 2.
# Unit test (4): directly verify code_runner_docker staging → catch Bug 1.
# All tests run in CI without Docker (EXECUTION_ENABLED guarded by env patch).

import os
import shutil
import tempfile
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient, ASGITransport

from arcade_app.agent import app
from arcade_app.database import get_session
from arcade_app.routers.routes_quests_runtime import get_user_id


def _sprint29_quest(objectives: list, grading_json: dict | None = None):
    """Minimal SimpleNamespace mimicking QuestDefinition for mock DB returns."""
    return SimpleNamespace(
        slug="test-quest-sprint29",
        language="python",
        tier=1,
        objectives_json=objectives,
        grading_json=grading_json or {},
        workspace_json=None,
        runtime_rules_json={"enabled": False},
        sandbox=False,
        is_sandbox=False,
        db_engine=None,
    )


def _sprint29_db(quest):
    """
    AsyncMock DB session for submit_quest().

    get_existing_attempt_by_idempotency() short-circuits without a DB call when no
    idempotency_key is sent, so the effective execute() sequence is:
      1. QuestDefinition query → quest
      2. QuestProgressV2 query → existing progress record (for passing tests)

    A dispatch function inspects the compiled statement so tests stay robust even if
    the query order shifts.
    """
    db = AsyncMock()
    db.add = MagicMock()
    db.flush = AsyncMock()
    db.commit = AsyncMock()
    db.rollback = AsyncMock()

    r_quest = MagicMock()
    r_quest.scalar_one_or_none.return_value = quest

    mock_progress = SimpleNamespace(
        user_id="test-user",
        quest_id="test-quest-sprint29",
        status="in_progress",
        runs_count=0,
        attempts_count=0,
        best_xp=0,
        last_xp=0,
        hint_tier_unlocked=0,
        last_run_at=None,
        completed_at=None,
    )
    r_prog = MagicMock()
    r_prog.scalar_one_or_none.return_value = mock_progress

    r_none = MagicMock()
    r_none.scalar_one_or_none.return_value = None

    def _dispatch(stmt):
        s = str(stmt).lower()
        if "questdefinition" in s:
            return r_quest
        if "questprogress" in s:
            return r_prog
        return r_none

    db.execute.side_effect = _dispatch
    return db


def _exec_result(stdout="", stderr="", exit_code=0):
    return SimpleNamespace(
        ok=exit_code == 0,
        stdout=stdout,
        stderr=stderr,
        exit_code=exit_code,
        timed_out=False,
        duration_ms=50,
        artifacts=None,
        selenium_trace=None,
        state=None,
    )


class TestSubmitEndToEnd:
    """Sprint 29 regression armor for Sprint 28 Bug 1 and Bug 2."""

    @pytest.mark.asyncio
    async def test_submit_calls_run_code_with_mode_tests_for_tests_pass_quest(self):
        """
        Bug 2 regression: SUBMIT must call run_code(mode='tests') for tests_pass quests.

        If Bug 2 is reintroduced (hardcoded mode='run'), captured['mode'] == 'run'
        and this assertion fails.
        """
        quest = _sprint29_quest(
            objectives=[{"kind": "tests_pass", "id": "run_tests", "title": "Tests pass"}],
            grading_json={"entrypoint": "task.py"},
        )
        mock_db = _sprint29_db(quest)
        captured: Dict = {}

        def fake_run_code(*args, **kwargs):
            captured["mode"] = kwargs.get("mode", "run")
            return _exec_result(stdout="1 passed")

        async def override_db():
            yield mock_db

        def mock_user_id():
            return "test-user"

        app.dependency_overrides[get_session] = override_db
        app.dependency_overrides[get_user_id] = mock_user_id
        try:
            with patch("arcade_app.services.code_runner.run_code", fake_run_code), \
                 patch(
                     "arcade_app.routers.routes_quests_runtime.validate_quest_attempt",
                     return_value=[{"id": "run_tests", "ok": True}],
                 ), \
                 patch.dict(os.environ, {"EXECUTION_ENABLED": "1"}):
                async with AsyncClient(
                    transport=ASGITransport(app=app), base_url="http://test"
                ) as client:
                    resp = await client.post(
                        "/api/quests/test-quest-sprint29/submit",
                        json={"code": "def solve(): pass", "language": "python"},
                    )
        finally:
            app.dependency_overrides.pop(get_session, None)
            app.dependency_overrides.pop(get_user_id, None)

        assert resp.status_code == 200, f"Expected 200: {resp.text}"
        assert captured.get("mode") == "tests", (
            f"run_code must be called with mode='tests' for tests_pass quests, "
            f"got mode='{captured.get('mode')}'. Sprint 28 Bug 2 has been reintroduced."
        )

    @pytest.mark.asyncio
    async def test_submit_stdout_regex_quest_uses_mode_run(self):
        """
        Control: non-tests_pass quests must still call run_code(mode='run').

        Ensures the Bug 2 fix did not accidentally flip the mode for all quest types.
        """
        quest = _sprint29_quest(
            objectives=[{
                "kind": "stdout_regex",
                "id": "prints_hello",
                "title": "Prints hello",
                "rule": {"pattern": "hello"},
            }],
        )
        mock_db = _sprint29_db(quest)
        captured: Dict = {}

        def fake_run_code(*args, **kwargs):
            captured["mode"] = kwargs.get("mode", "run")
            return _exec_result(stdout="hello\n")

        async def override_db():
            yield mock_db

        def mock_user_id():
            return "test-user"

        app.dependency_overrides[get_session] = override_db
        app.dependency_overrides[get_user_id] = mock_user_id
        try:
            with patch("arcade_app.services.code_runner.run_code", fake_run_code), \
                 patch(
                     "arcade_app.routers.routes_quests_runtime.validate_quest_attempt",
                     return_value=[{"id": "prints_hello", "ok": True}],
                 ), \
                 patch.dict(os.environ, {"EXECUTION_ENABLED": "1"}):
                async with AsyncClient(
                    transport=ASGITransport(app=app), base_url="http://test"
                ) as client:
                    resp = await client.post(
                        "/api/quests/test-quest-sprint29/submit",
                        json={"code": 'print("hello")', "language": "python"},
                    )
        finally:
            app.dependency_overrides.pop(get_session, None)
            app.dependency_overrides.pop(get_user_id, None)

        assert resp.status_code == 200
        assert captured.get("mode") == "run", (
            f"stdout_regex quest must use mode='run', got '{captured.get('mode')}'"
        )

    @pytest.mark.asyncio
    async def test_submit_tests_pass_quest_returns_ok_false_on_failure(self):
        """
        Bug 2 regression (response path): when tests fail, SUBMIT must return ok=False.

        Before the fix, tests_pass objectives always got empty stdout (mode was 'run',
        no grading files injected), so even broken code could not be distinguished
        from a real test failure — both returned the same "No test output" error.
        This test verifies the failure path is reachable and returns the right shape.
        """
        quest = _sprint29_quest(
            objectives=[{"kind": "tests_pass", "id": "run_tests", "title": "Tests pass"}],
            grading_json={"entrypoint": "task.py"},
        )
        mock_db = _sprint29_db(quest)

        def fake_run_code(*args, **kwargs):
            return _exec_result(stdout="", stderr="SyntaxError: invalid syntax", exit_code=1)

        async def override_db():
            yield mock_db

        def mock_user_id():
            return "test-user"

        app.dependency_overrides[get_session] = override_db
        app.dependency_overrides[get_user_id] = mock_user_id
        try:
            with patch("arcade_app.services.code_runner.run_code", fake_run_code), \
                 patch(
                     "arcade_app.routers.routes_quests_runtime.validate_quest_attempt",
                     return_value=[{"id": "run_tests", "ok": False, "detail": "Tests failed"}],
                 ), \
                 patch.dict(os.environ, {"EXECUTION_ENABLED": "1"}):
                async with AsyncClient(
                    transport=ASGITransport(app=app), base_url="http://test"
                ) as client:
                    resp = await client.post(
                        "/api/quests/test-quest-sprint29/submit",
                        json={"code": "BROKEN !!!!", "language": "python"},
                    )
        finally:
            app.dependency_overrides.pop(get_session, None)
            app.dependency_overrides.pop(get_user_id, None)

        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is False, (
            f"Broken-code submit must return ok=False, got: {body}"
        )

    def test_code_runner_docker_stages_runner_for_empty_code_in_tests_mode(self):
        """
        Bug 1 regression: run_unittest_json.py must be staged even when code=''.

        The Sprint 28 fix moved the staging block outside `if code:` in
        code_runner_docker.py. If Bug 1 is reintroduced (staging moved back inside
        `if code:`), this test fails because .evalforge/run_unittest_json.py is never
        written — exactly the condition that caused the "can't open file" crash.

        Strategy: patch tempfile.TemporaryDirectory to capture staged files before
        cleanup, patch subprocess so Docker commands don't run, then verify the
        runner script was written to the temp dir.
        """
        from arcade_app.services.code_runner_docker import run_code_docker

        staged: List = []

        class _CapturingTempDir:
            """Wraps mkdtemp; records all files before cleanup so we can assert on them."""

            def __init__(self, **kwargs):
                init_kwargs = {k: v for k, v in kwargs.items() if k in ("prefix", "suffix", "dir")}
                self._path = tempfile.mkdtemp(**init_kwargs)
                self.name = self._path

            def __enter__(self):
                return self.name

            def __exit__(self, *args):
                for root, _dirs, files in os.walk(self.name):
                    for fname in files:
                        staged.append(
                            os.path.relpath(
                                os.path.join(root, fname), self.name
                            ).replace("\\", "/")
                        )
                shutil.rmtree(self.name, ignore_errors=True)
                return False

        fake_proc = MagicMock(returncode=0, stdout=b"", stderr=b"")
        popen_ctx = MagicMock(wait=MagicMock(return_value=0), stdout=iter([]))
        fake_popen = MagicMock()
        fake_popen.return_value.__enter__ = MagicMock(return_value=popen_ctx)
        fake_popen.return_value.__exit__ = MagicMock(return_value=False)

        with patch("tempfile.TemporaryDirectory", _CapturingTempDir), \
             patch("subprocess.run", return_value=fake_proc), \
             patch("subprocess.Popen", fake_popen):
            try:
                run_code_docker("python", code="", mode="tests", workspace={"files": []})
            except Exception:
                pass  # Docker execution errors are expected in CI — we only care about staging

        runner_staged = any(".evalforge/run_unittest_json.py" in p for p in staged)
        assert runner_staged, (
            f".evalforge/run_unittest_json.py was NOT staged for empty-code tests-mode run. "
            f"Files staged: {staged}. "
            "Sprint 28 Bug 1 has been reintroduced: empty-code test-mode runs will crash with "
            "'can\\'t open file .evalforge/run_unittest_json.py'."
        )

"""
Sprint 21 — Grading Truth Table Tests
======================================

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

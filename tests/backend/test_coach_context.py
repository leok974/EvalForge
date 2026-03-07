"""
Coach Context Hardening — Unit Tests (no Gemini calls)

A: Pass + debug mode → deterministic _passed_fallback (PASS_NO_DEBUG_NEEDED)
B: Entrypoint file surfaces first in built prompt with [ENTRYPOINT] marker
C: Wrong-target edit suggestion gets overridden to entrypoint_path by guardrail
"""
import sys
import os
import pathlib
import pytest
from unittest.mock import MagicMock

# Ensure arcade_app is importable from repo root
REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from arcade_app.schemas.coach_schemas import (
    CoachRequest, CoachResponse, Hypothesis, NextStep, SafetyAssessment
)
from arcade_app.services import coach_prompts
from arcade_app.services.coach_service import CoachService


def _make_req(**kwargs) -> CoachRequest:
    defaults = dict(
        mode="debug",
        world="sql",
        quest_slug="sql-select",
        student_mode=True,
        workspace_files=[
            {"path": "task.sql", "content": "SELECT name, city FROM users ORDER BY name;"},
            {"path": "query.sql", "content": "SELECT * FROM people;"},
        ],
    )
    defaults.update(kwargs)
    return CoachRequest(**defaults)


# ---------------------------------------------------------------------------
# Test A: pass + debug → deterministic "nothing to debug" without Gemini call
# ---------------------------------------------------------------------------

def test_passed_debug_returns_deterministic_response():
    """run_passed=True in debug mode must return _passed_fallback (no AI call)."""
    svc = CoachService()
    svc.enabled = True
    # Even if client is mock, G0 should short-circuit before calling it
    svc.client = MagicMock()

    req = _make_req(mode="debug", run_passed=True)
    import asyncio
    result = asyncio.get_event_loop().run_until_complete(svc.process_request(req))

    assert result.failure_class == "PASS_NO_DEBUG_NEEDED"
    assert result.confidence == 1.0
    # Must not have called Gemini
    svc.client.models.generate_content.assert_not_called()


# ---------------------------------------------------------------------------
# Test B: entrypoint file appears first in prompt with [ENTRYPOINT] marker
# ---------------------------------------------------------------------------

def test_prompt_surfaces_entrypoint_first():
    """task.sql must appear before query.sql in the built prompt, with [ENTRYPOINT] label."""
    req = _make_req(entrypoint_path="task.sql", language="sql")
    prompt = coach_prompts.build_user_prompt(req.model_dump())

    entrypoint_pos = prompt.find("[ENTRYPOINT]")
    query_pos = prompt.find("query.sql")

    assert entrypoint_pos != -1, "Prompt must contain [ENTRYPOINT] marker"
    assert entrypoint_pos < query_pos, (
        f"[ENTRYPOINT] section ({entrypoint_pos}) must appear before query.sql ({query_pos})"
    )


def test_prompt_includes_allowed_edit_targets():
    """Prompt must declare ALLOWED_EDIT_TARGETS so the model knows the constraint."""
    req = _make_req(entrypoint_path="task.sql", language="sql")
    prompt = coach_prompts.build_user_prompt(req.model_dump())

    assert "ALLOWED_EDIT_TARGETS" in prompt
    assert "task.sql" in prompt


def test_prompt_excludes_fixture_files():
    """schema.sql / seed.sql fixture files should NOT appear as editable workspace files."""
    req = CoachRequest(
        mode="debug",
        world="sql",
        quest_slug="sql-select",
        student_mode=True,
        entrypoint_path="task.sql",
        language="sql",
        workspace_files=[
            {"path": "task.sql", "content": "SELECT name FROM users;"},
            {"path": "fixtures/schema.sql", "content": "CREATE TABLE users (...)"},
            {"path": "fixtures/seed.sql", "content": "INSERT INTO users ..."},
        ],
    )
    prompt = coach_prompts.build_user_prompt(req.model_dump())

    # Fixtures must not show up in the editable reference block
    assert "[REFERENCE ONLY" not in prompt or "fixtures/schema.sql" not in prompt.split("[REFERENCE ONLY")[1].split("[CONSTRAINTS]")[0]


# ---------------------------------------------------------------------------
# Test C: wrong-target edit suggestion gets overridden to entrypoint_path
# ---------------------------------------------------------------------------

def test_guardrail_overrides_wrong_edit_target():
    """If model returns next_step targeting query.sql, guardrail rewrites it to task.sql."""
    svc = CoachService()
    svc.enabled = True

    # Mock Gemini returning a next_step pointing to the wrong file
    bad_response = CoachResponse(
        mode="debug",
        summary_md="The issue is in your query.",
        hypotheses=[],
        next_steps=[
            NextStep(label="Fix the query", action="edit", target="query.sql"),
            NextStep(label="Re-run", action="run", target=None),
        ],
        patch=None,
        confidence=0.8,
        safety=SafetyAssessment(solution_leak_risk="low", blocked=False),
        evidence=["some error line"],
    )

    mock_response = MagicMock()
    mock_response.parsed = bad_response
    svc.client = MagicMock()
    svc.client.models.generate_content.return_value = mock_response

    req = _make_req(
        mode="debug",
        run_passed=False,
        entrypoint_path="task.sql",
        runner_result={"passed": False, "exit_code": 1},
        terminal_output_text="some error",
    )

    import asyncio
    result = asyncio.get_event_loop().run_until_complete(svc.process_request(req))

    edit_steps = [s for s in result.next_steps if s.action == "edit"]
    assert all(s.target == "task.sql" for s in edit_steps), (
        f"All edit steps must target task.sql, got: {[s.target for s in edit_steps]}"
    )
    # Guardrail should be recorded in failure_class
    assert "coach_guardrail:edit_target_overridden_to_task.sql" in (result.failure_class or "")

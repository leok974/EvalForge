"""
tests/test_objectives_serializer_shape.py

Regression guard for the objectives serializer shape contract.

Prevents the "count is right but rows are empty shells" bug from
silently coming back.  The fix lives in:
  arcade_app/quest_helper._normalize_objectives()

The stable frontend contract is:
  { id, text, validator: { kind, value } }
"""
import sys, os
sys.path.insert(0, os.path.abspath('.'))

import pytest
from arcade_app.quest_helper import _normalize_objectives


# ---------------------------------------------------------------------------
# Old frontend format: passthrough unchanged
# ---------------------------------------------------------------------------

def test_old_shape_text_passthrough():
    objs = [
        {"id": "o1", "text": "Do X", "validator": {"kind": "source_regex", "value": "foo"}}
    ]
    out = _normalize_objectives(objs)
    assert len(out) == 1
    assert out[0]["text"] == "Do X"
    assert out[0]["validator"]["kind"] == "source_regex"
    assert out[0]["validator"]["value"] == "foo"


def test_old_shape_preserves_why():
    objs = [
        {"id": "o2", "text": "Define main()", "why": "Entry point", "validator": {"kind": "ast", "value": "main"}}
    ]
    out = _normalize_objectives(objs)
    assert out[0]["why"] == "Entry point"


# ---------------------------------------------------------------------------
# New DB format: {id, title, kind, rule} → normalize to frontend contract
# ---------------------------------------------------------------------------

def test_new_shape_source_regex():
    objs = [{"id": "obj_syntax", "title": "Uses OVER + PARTITION BY", "kind": "source_regex",
              "rule": {"pattern": r"OVER\s*\("}}]
    out = _normalize_objectives(objs)
    obj = out[0]
    assert obj["id"] == "obj_syntax"
    assert obj["text"] == "Uses OVER + PARTITION BY"
    assert obj["validator"]["kind"] == "source_regex"
    assert obj["validator"]["value"] == r"OVER\s*\("


def test_new_shape_exit_code_zero():
    objs = [{"id": "obj_runs", "title": "Executes without errors", "kind": "exit_code_zero", "rule": {}}]
    out = _normalize_objectives(objs)
    assert out[0]["text"] == "Executes without errors"
    assert out[0]["validator"]["kind"] == "exit_code_zero"
    assert out[0]["validator"]["value"] == "0"


def test_new_shape_tests_pass():
    objs = [{"id": "obj_tests", "title": "All tests pass", "kind": "tests_pass",
              "rule": {"test_file": "test_solution.py"}}]
    out = _normalize_objectives(objs)
    assert out[0]["validator"]["kind"] == "tests_pass"
    assert out[0]["validator"]["value"] == "test_solution.py"


def test_new_shape_ast():
    objs = [{"id": "obj_ast", "title": "Defines main function", "kind": "ast",
              "rule": {"must_define_function": "main"}}]
    out = _normalize_objectives(objs)
    assert out[0]["validator"]["kind"] == "ast"
    assert out[0]["validator"]["value"] == "main"


def test_new_shape_stdout_regex():
    objs = [{"id": "obj_out", "title": "Prints hello", "kind": "stdout_regex",
              "rule": {"pattern": "hello"}}]
    out = _normalize_objectives(objs)
    assert out[0]["validator"]["kind"] == "stdout_regex"
    assert out[0]["validator"]["value"] == "hello"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_empty_list():
    assert _normalize_objectives([]) == []


# ---------------------------------------------------------------------------
# Incident test — named for archaeology
# INCIDENT: objectives_ui_blank_rows (2026-02-25)
# Symptom: "count is right but rows are empty shells"
#   — QuestDrawer shows "0/2 objectives" but both rows have no text
# Root cause: quest_helper returned raw DB format {title, kind, rule} but
#   QuestDrawer reads obj.text (undefined → empty) and obj.validator (undefined
#   → client-side checks all fail silently)
# Fix: _normalize_objectives() in quest_helper.py
# ---------------------------------------------------------------------------

def test_incident_count_correct_row_blank():
    """
    Regression for the exact "count right, rows blank" incident.

    The Phase Debt-2 backfill stored objectives in new DB format.
    The serializer returned them raw. QuestDrawer renders obj.text
    which was undefined → silent empty shells, but len(quest.objectives)==2
    gave the correct count chip.
    """
    # Exact data shape produced by backfill_debt_wave.py
    new_format_objectives = [
        {
            "id": "obj_runs",
            "title": "Query executes without errors",   # <-- NOT "text"
            "kind": "exit_code_zero",
            "rule": {"kind": "exit_code_zero"}
        },
        {
            "id": "obj_syntax",
            "title": "Uses a window function with OVER + PARTITION BY",
            "kind": "source_regex",
            "rule": {
                "pattern": r"OVER\s*\(",
                "description": "Query uses OVER + PARTITION BY"
            }
        }
    ]

    out = _normalize_objectives(new_format_objectives)

    # Count is still 2 — this part was always correct
    assert len(out) == 2

    # THE FIX: both rows must now have "text" (what QuestDrawer renders)
    assert out[0]["text"] == "Query executes without errors"
    assert out[1]["text"] == "Uses a window function with OVER + PARTITION BY"

    # AND validator must be a dict with kind (what QuestIDE uses for client checks)
    assert isinstance(out[0]["validator"], dict)
    assert out[0]["validator"]["kind"] == "exit_code_zero"
    assert isinstance(out[1]["validator"], dict)
    assert out[1]["validator"]["kind"] == "source_regex"




def test_non_dict_items_skipped():
    out = _normalize_objectives(["string", None, {"id": "o1", "text": "Fine", "validator": {"kind": "ast", "value": ""}}])
    assert len(out) == 1
    assert out[0]["id"] == "o1"


def test_mixed_old_and_new_in_same_quest():
    objs = [
        {"id": "old", "text": "Old format", "validator": {"kind": "contains", "value": "x"}},
        {"id": "new", "title": "New format", "kind": "source_regex", "rule": {"pattern": "SELECT"}},
    ]
    out = _normalize_objectives(objs)
    assert len(out) == 2
    assert out[0]["text"] == "Old format"
    assert out[1]["text"] == "New format"
    assert out[1]["validator"]["kind"] == "source_regex"


def test_title_fallback_to_id_when_missing():
    """If somehow neither text nor title is present, id is used as fallback."""
    objs = [{"id": "obj_runs", "kind": "exit_code_zero", "rule": {}}]
    out = _normalize_objectives(objs)
    assert out[0]["text"] == "obj_runs"


def test_output_always_has_id_text_validator():
    """Shape contract: every output item must have id, text, validator with kind."""
    objs = [
        {"id": "a", "title": "A title", "kind": "source_regex", "rule": {"pattern": "foo"}},
        {"id": "b", "text": "B text", "validator": {"kind": "ast", "value": "bar"}},
    ]
    for obj in _normalize_objectives(objs):
        assert "id" in obj
        assert "text" in obj
        assert "validator" in obj
        assert "kind" in obj["validator"]

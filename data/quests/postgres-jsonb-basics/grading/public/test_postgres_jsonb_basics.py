"""
Grading test for postgres-jsonb-basics.
Source-check test: verifies the SQL uses the JSONB ->> extraction operator.
"""
import re
import pytest
from pathlib import Path

QUEST_DIR = Path(__file__).resolve().parents[2]
TASK_SQL  = QUEST_DIR / "workspace" / "task.sql"


def read_task() -> str:
    assert TASK_SQL.exists(), f"workspace/task.sql not found: {TASK_SQL}"
    return TASK_SQL.read_text(encoding="utf-8")


def test_uses_jsonb_extraction_operator():
    sql = read_task()
    # Strip comments before checking — operator must appear as real SQL
    uncommented = re.sub(r"--[^\n]*", "", sql)
    assert re.search(r"->>", uncommented), \
        "Expected JSONB ->> operator for text field extraction (not just in a TODO comment)"


def test_filters_by_status():
    sql = read_task()
    # Strip comments before checking
    uncommented = re.sub(r"--[^\n]*", "", sql)
    assert re.search(r"(?i)status", uncommented), \
        "Expected WHERE clause filtering by payload status (not just in a comment)"

"""
Grading test for postgres-explain-basics.
Source-check test: verifies the SQL uses the EXPLAIN keyword.
"""
import re
import pytest
from pathlib import Path

QUEST_DIR = Path(__file__).resolve().parents[2]
TASK_SQL  = QUEST_DIR / "workspace" / "task.sql"


def read_task() -> str:
    assert TASK_SQL.exists(), f"workspace/task.sql not found: {TASK_SQL}"
    return TASK_SQL.read_text(encoding="utf-8")


def test_uses_explain():
    sql = read_task()
    # Strip comments before checking — EXPLAIN must appear as real SQL
    uncommented = re.sub(r"--[^\n]*", "", sql)
    assert re.search(r"(?i)\bEXPLAIN\b", uncommented), \
        "Expected EXPLAIN keyword at the start of the query (not just in a TODO comment)"

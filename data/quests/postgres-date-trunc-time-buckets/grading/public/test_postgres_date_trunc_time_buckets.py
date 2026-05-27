"""
Grading test for postgres-date-trunc-time-buckets.
Source-check test: verifies the SQL uses DATE_TRUNC and GROUP BY correctly.
"""
import re
import pytest
from pathlib import Path

QUEST_DIR = Path(__file__).resolve().parents[2]
TASK_SQL  = QUEST_DIR / "workspace" / "task.sql"


def read_task() -> str:
    assert TASK_SQL.exists(), f"workspace/task.sql not found: {TASK_SQL}"
    return TASK_SQL.read_text(encoding="utf-8")


def test_uses_date_trunc():
    sql = read_task()
    assert re.search(r"(?i)DATE_TRUNC", sql), \
        "Expected DATE_TRUNC('hour', ...) in solution"


def test_uses_group_by():
    sql = read_task()
    # Strip comments before checking — GROUP BY must appear as real SQL
    uncommented = re.sub(r"--[^\n]*", "", sql)
    assert re.search(r"(?i)GROUP\s+BY", uncommented), \
        "Expected GROUP BY clause for hourly aggregation (not just in a comment)"

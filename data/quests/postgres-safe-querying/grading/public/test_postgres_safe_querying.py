"""
Grading test for postgres-safe-querying.
Source-check test: verifies the SQL uses information_schema and LIMIT correctly.
"""
import re
import pytest
from pathlib import Path

QUEST_DIR = Path(__file__).resolve().parents[2]
TASK_SQL  = QUEST_DIR / "workspace" / "task.sql"


def read_task() -> str:
    assert TASK_SQL.exists(), f"workspace/task.sql not found: {TASK_SQL}"
    return TASK_SQL.read_text(encoding="utf-8")


def test_uses_information_schema():
    sql = read_task()
    assert re.search(r"(?i)information_schema", sql), \
        "Expected SQL to query information_schema"


def test_selects_required_columns():
    sql = read_task()
    assert re.search(r"(?i)column_name", sql), "Expected column_name in SELECT"
    assert re.search(r"(?i)data_type", sql), "Expected data_type in SELECT"
    assert re.search(r"(?i)is_nullable", sql), "Expected is_nullable in SELECT"


def test_uses_limit():
    sql = read_task()
    # Strip comments before checking — LIMIT must appear as real SQL, not just in a TODO comment
    uncommented = re.sub(r"--[^\n]*", "", sql)
    assert re.search(r"(?i)\bLIMIT\b", uncommented), "Expected LIMIT clause for safe preview (not just in a comment)"

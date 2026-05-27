"""
Grading test for sql-t2-upsert-on-conflict.
Source-check test: verifies the SQL uses ON CONFLICT ... DO UPDATE with the
excluded pseudo-table for upsert semantics.
SQLite execution is skipped — ON CONFLICT DO UPDATE with excluded is Postgres-specific
multi-statement syntax that SQLite's execute() cannot handle.
"""
import re
import pytest
from pathlib import Path

QUEST_DIR = Path(__file__).resolve().parents[2]
TASK_SQL  = QUEST_DIR / "workspace" / "task.sql"


def read_task() -> str:
    assert TASK_SQL.exists(), f"workspace/task.sql not found: {TASK_SQL}"
    return TASK_SQL.read_text(encoding="utf-8")


def uncommented(sql: str) -> str:
    """Strip single-line SQL comments so TODO hints don't trigger assertions."""
    return re.sub(r"--[^\n]*", "", sql)


def test_uses_on_conflict():
    sql = uncommented(read_task())
    assert re.search(r"(?i)\bON\s+CONFLICT\b", sql), \
        "Expected ON CONFLICT clause for upsert (not just in a TODO comment)"


def test_uses_do_update():
    sql = uncommented(read_task())
    assert re.search(r"(?i)\bDO\s+UPDATE\b", sql), \
        "Expected DO UPDATE action on conflict"


def test_uses_excluded_alias():
    sql = uncommented(read_task())
    assert re.search(r"(?i)\bexcluded\b", sql), \
        "Expected 'excluded' pseudo-table to reference the conflicting row's values"

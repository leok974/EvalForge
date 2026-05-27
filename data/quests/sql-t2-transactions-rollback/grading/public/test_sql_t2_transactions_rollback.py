"""
Grading test for sql-t2-transactions-rollback.
Source-check test: verifies the SQL uses BEGIN and ROLLBACK to wrap statements
in a transaction that is intentionally undone.
SQLite execution is skipped — multi-statement transaction scripts cannot be
executed via a single sqlite3.execute() call.
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


def test_uses_begin():
    sql = uncommented(read_task())
    assert re.search(r"(?i)\bBEGIN\b", sql), \
        "Expected BEGIN (or BEGIN TRANSACTION) to open the transaction block"


def test_uses_rollback():
    sql = uncommented(read_task())
    assert re.search(r"(?i)\bROLLBACK\b", sql), \
        "Expected ROLLBACK to undo the transaction (not just in a TODO comment)"

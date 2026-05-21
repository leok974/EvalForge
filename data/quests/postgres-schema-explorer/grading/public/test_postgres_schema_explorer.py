"""
Public grading tests for postgres-schema-explorer.

Tests use an in-memory SQLite DB with a simplified schema matching the
Postgres fixture structure. The JOIN / WHERE / ORDER BY logic is standard SQL
and runs identically on both SQLite and Postgres.
"""
import pytest
import sqlite3
from pathlib import Path

QUEST_DIR = Path(__file__).resolve().parents[2]
TASK_SQL = QUEST_DIR / "workspace" / "task.sql"

# SQLite-compatible schema (subset of the Postgres schema.sql)
SQLITE_SCHEMA = """
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    department_id INTEGER REFERENCES departments(id)
);
"""

SQLITE_SEED = """
INSERT INTO departments (id, name) VALUES (1, 'Engineering'), (2, 'Marketing'), (3, 'Research');
INSERT INTO employees (name, email, department_id) VALUES
    ('Alice', 'alice@evalforge.com', 1),
    ('Bob',   'bob@evalforge.com',   1),
    ('Charlie','charlie@evalforge.com', 2),
    ('Diana', 'diana@evalforge.com', 3);
"""


def run_task_sql():
    """Load task.sql from workspace and execute it against the in-memory DB."""
    sql = TASK_SQL.read_text(encoding="utf-8")
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript(SQLITE_SCHEMA)
    cur.executescript(SQLITE_SEED)
    # Execute only the last statement in the file (the SELECT query)
    stmts = [s.strip() for s in sql.split(";") if s.strip()]
    select_stmt = next(
        (s for s in reversed(stmts) if s.upper().lstrip().startswith("SELECT")),
        None,
    )
    if not select_stmt:
        raise ValueError("No SELECT statement found in task.sql")
    cur.execute(select_stmt)
    rows = cur.fetchall()
    conn.close()
    return rows


def test_lists_engineering_employees():
    """Solution must return only the two Engineering employees."""
    rows = run_task_sql()
    names = [r[0] for r in rows]
    emails = [r[1] for r in rows]
    assert len(rows) == 2, f"EF_PSE_COUNT: expected 2 rows, got {len(rows)}: {rows}"
    assert names == ["Alice", "Bob"], f"EF_PSE_NAMES: expected ['Alice','Bob'], got {names}"
    assert "alice@evalforge.com" in emails, "EF_PSE_EMAIL_ALICE: alice@evalforge.com missing"
    assert "bob@evalforge.com" in emails, "EF_PSE_EMAIL_BOB: bob@evalforge.com missing"


def test_excludes_non_engineering():
    """Marketing and Research employees must NOT appear."""
    rows = run_task_sql()
    names = [r[0] for r in rows]
    assert "Charlie" not in names, "EF_PSE_EXCL_CHARLIE: Marketing employee should be excluded"
    assert "Diana" not in names, "EF_PSE_EXCL_DIANA: Research employee should be excluded"


def test_ordered_by_name():
    """Results must be sorted alphabetically by employee name."""
    rows = run_task_sql()
    names = [r[0] for r in rows]
    assert names == sorted(names), f"EF_PSE_ORDER: expected sorted names, got {names}"

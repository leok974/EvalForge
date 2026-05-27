"""
Grading test for postgres-real-schema-joins.
Uses an in-memory SQLite database with a compatible schema.
"""
import sqlite3
import pytest
from pathlib import Path

QUEST_DIR = Path(__file__).resolve().parents[2]
TASK_SQL  = QUEST_DIR / "workspace" / "task.sql"

SQLITE_SCHEMA = """
CREATE TABLE departments (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT
);
CREATE TABLE employees (
    id            INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    email         TEXT UNIQUE,
    department_id INTEGER REFERENCES departments(id)
);
CREATE TABLE projects (
    id     INTEGER PRIMARY KEY,
    name   TEXT NOT NULL,
    budget REAL NOT NULL
);
CREATE TABLE employee_assignments (
    employee_id INTEGER REFERENCES employees(id),
    project_id  INTEGER REFERENCES projects(id),
    role        TEXT,
    PRIMARY KEY (employee_id, project_id)
);
"""

SQLITE_SEED = """
INSERT INTO departments (id, name, location) VALUES
    (1, 'Engineering', 'San Francisco'),
    (2, 'Design',      'New York'),
    (3, 'Marketing',   'London');

INSERT INTO employees (id, name, email, department_id) VALUES
    (1, 'Alice Rivera',  'alice@evalforge.com',   1),
    (2, 'Bob Chen',      'bob@evalforge.com',     1),
    (3, 'Charlie Davis', 'charlie@evalforge.com', 2),
    (4, 'Diana Prince',  'diana@evalforge.com',   3);

INSERT INTO projects (id, name, budget) VALUES
    (1, 'Project Phoenix', 120000.0),
    (2, 'Project Icarus',   45000.0),
    (3, 'Project Chronos',  30000.0);

INSERT INTO employee_assignments (employee_id, project_id, role) VALUES
    (1, 1, 'Lead Engineer'),
    (2, 1, 'QA'),
    (3, 1, 'UI Designer'),
    (1, 2, 'Consultant'),
    (2, 3, 'DevOps'),
    (4, 3, 'Campaign Manager');
"""


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(SQLITE_SCHEMA + SQLITE_SEED)
    yield conn
    conn.close()


def test_task_file_exists():
    assert TASK_SQL.exists(), f"workspace/task.sql not found: {TASK_SQL}"


def test_returns_three_rows(db):
    sql = TASK_SQL.read_text(encoding="utf-8")
    rows = db.execute(sql).fetchall()
    assert len(rows) == 3, f"Expected 3 rows for budget > 50000, got {len(rows)}"


def test_required_columns(db):
    sql = TASK_SQL.read_text(encoding="utf-8")
    rows = db.execute(sql).fetchall()
    assert len(rows) > 0
    cols = rows[0].keys()
    assert "employee_name" in cols, "Missing column: employee_name"
    assert "department_name" in cols, "Missing column: department_name"
    assert "project_name" in cols, "Missing column: project_name"
    assert "role" in cols, "Missing column: role"


def test_only_phoenix_project(db):
    """All returned rows should be for Project Phoenix (budget=120000)."""
    sql = TASK_SQL.read_text(encoding="utf-8")
    rows = db.execute(sql).fetchall()
    for row in rows:
        assert row["project_name"] == "Project Phoenix", \
            f"Unexpected project: {row['project_name']} — only high-budget projects should appear"


def test_chronos_excluded(db):
    """Project Chronos (budget=30000) must not appear."""
    sql = TASK_SQL.read_text(encoding="utf-8")
    rows = db.execute(sql).fetchall()
    names = [r["project_name"] for r in rows]
    assert "Project Chronos" not in names, "Project Chronos (low budget) should be excluded"

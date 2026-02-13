
import pytest
from pathlib import Path
from data._shared.sql_test_helpers import run_sql as base_run_sql, assert_rows_match

QUEST_DIR = Path(__file__).resolve().parents[2]
# Using task.sql in workspace (swapped in solution mode)
TASK_SQL = QUEST_DIR / "workspace" / "task.sql"
SCHEMA_SQL = QUEST_DIR / "fixtures" / "schema.sql"
SEED_SQL = QUEST_DIR / "fixtures" / "seed.sql"

@pytest.fixture
def run_sql():
    return lambda: base_run_sql(TASK_SQL, SCHEMA_SQL, SEED_SQL)


def test_sql_ignition(run_sql):
    rows = run_sql()
    assert len(rows) == 6
    # Check first row
    assert rows[0] == (1, 'Alice', 'alice@example.com', 28, 'Detroit', 1)
    # Check columns count
    assert len(rows[0]) == 6


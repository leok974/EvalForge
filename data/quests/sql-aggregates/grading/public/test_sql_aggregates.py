
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


def test_sql_aggregates(run_sql):
    rows = run_sql()
    assert len(rows) == 1
    # Paid orders:
    # 1: 102400
    # 3: 9900
    # 5: 1700
    # Sum: 114000
    # Count: 3
    # Avg: 38000
    assert rows[0] == (3, 114000, 38000.0)


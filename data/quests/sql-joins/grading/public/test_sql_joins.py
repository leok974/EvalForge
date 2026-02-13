
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


def test_sql_joins(run_sql):
    rows = run_sql()
    assert len(rows) == 3
    # 1 (Alice), 3 (Bob), 5 (Diana)
    assert rows[0] == (1, 'Alice', 102400)
    assert rows[1] == (3, 'Bob', 9900)
    assert rows[2] == (5, 'Diana', 1700)


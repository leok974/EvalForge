
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


def test_sql_order_limit(run_sql):
    rows = run_sql()
    assert len(rows) == 3
    # 1. Laptop (99900)
    # 2. Mouse (2500)
    # 3. Coffee (1200) -- Notebook is 500. Headphones discontinued.
    assert rows[0] == (1, 'Laptop', 99900)
    assert rows[1] == (2, 'Mouse', 2500)
    assert rows[2] == (3, 'Coffee', 1200)


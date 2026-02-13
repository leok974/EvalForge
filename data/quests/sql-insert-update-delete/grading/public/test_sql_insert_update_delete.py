
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


def test_sql_insert_update_delete(run_sql):
    rows = run_sql()
    # 1. Laptop (99900)
    # 2. Mouse (2600) - Updated
    # 3. Coffee (1200)
    # 4. Deleted
    # 5. Notebook (500)
    # 6. Pen (300) - Inserted
    
    assert len(rows) == 5
    assert rows[0] == (1, 'Laptop', 99900)
    assert rows[1] == (2, 'Mouse', 2600)
    assert rows[2] == (3, 'Coffee', 1200)
    assert rows[3] == (5, 'Notebook', 500)
    assert rows[4] == (6, 'Pen', 300)


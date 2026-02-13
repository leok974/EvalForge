
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


def test_sql_left_join_null(run_sql):
    rows = run_sql()
    # Users:
    # 1 Alice (Has order)
    # 2 Bob (Has order)
    # 3 Charlie (No order, but inactive)
    # 4 Diana (Has order)
    # 5 Evan (Has order, inactive) ?? Order 6 is Evan.
    # 6 Fay (Active, no orders)
    
    # Wait, check seed:
    # Orders: 1->1, 2->1, 3->2, 4->3, 5->4, 6->5.
    # User 6 (Fay) has no orders.
    # User 3 (Charlie) has order 4 (cancelled), but user 3 is inactive.
    # We want ACTIVE users with no orders.
    # Fay is active (1).
    
    assert len(rows) == 1
    assert rows[0] == (6, 'Fay')


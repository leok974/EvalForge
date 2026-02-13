
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


def test_sql_where(run_sql):
    rows = run_sql()
    # Alice is 28, Detroit, Active -> Match
    # Charlie is 22, Detroit, Inactive -> No
    # Others don't match city or active
    # Only Alice matches strict criteria? 
    # Let's check seed:
    # 1: Alice, 28, Detroit, 1 -> Yes
    # 3: Charlie, 22, Detroit, 0 -> No (inactive, age<25)
    
    # Wait, spec says age >= 25.
    assert len(rows) == 1
    assert rows[0] == (1, 'Alice', 28)


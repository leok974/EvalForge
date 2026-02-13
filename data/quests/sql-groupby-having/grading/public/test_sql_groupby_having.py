
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


def test_sql_groupby_having(run_sql):
    rows = run_sql()
    # Detroit: 2 (Alice, Charlie)
    # Austin: 2 (Bob, Evan)
    # Others are 1
    # Order: count DESC -> both 2. Then city ASC -> Austin, Detroit.
    assert len(rows) == 2
    assert rows[0] == ('Austin', 2)
    assert rows[1] == ('Detroit', 2)


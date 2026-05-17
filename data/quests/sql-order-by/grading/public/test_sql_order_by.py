import pytest
from pathlib import Path
from data._shared.sql_test_helpers import run_sql as base_run_sql

QUEST_DIR = Path(__file__).resolve().parents[2]
TASK_SQL = QUEST_DIR / "workspace" / "task.sql"
SCHEMA_SQL = QUEST_DIR / "fixtures" / "schema.sql"
SEED_SQL = QUEST_DIR / "fixtures" / "seed.sql"


@pytest.fixture
def run_sql():
    return lambda: base_run_sql(TASK_SQL, SCHEMA_SQL, SEED_SQL)


def test_sql_order_by(run_sql):
    rows = run_sql()
    # 6 users sorted by city ASC, then name ASC within same city:
    # Austin: Bob (35), Evan (29)
    # Detroit: Alice (28), Charlie (22)
    # Miami: Fay (33)
    # Seattle: Diana (41)
    assert len(rows) == 6
    assert rows[0] == ('Austin', 'Bob')
    assert rows[1] == ('Austin', 'Evan')
    assert rows[2] == ('Detroit', 'Alice')
    assert rows[3] == ('Detroit', 'Charlie')
    assert rows[4] == ('Miami', 'Fay')
    assert rows[5] == ('Seattle', 'Diana')

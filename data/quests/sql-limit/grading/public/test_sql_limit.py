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


def test_sql_limit(run_sql):
    rows = run_sql()
    # Active products (is_discontinued=0): Laptop (99900), Mouse (2500), Coffee (1200), Notebook (500)
    # Top 3 by price_cents DESC:
    # 1. Laptop  (id=1, electronics, 99900)
    # 2. Mouse   (id=2, electronics, 2500)
    # 3. Coffee  (id=3, grocery,     1200)
    assert len(rows) == 3
    assert rows[0] == (1, 'Laptop', 'electronics', 99900)
    assert rows[1] == (2, 'Mouse', 'electronics', 2500)
    assert rows[2] == (3, 'Coffee', 'grocery', 1200)

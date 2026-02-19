
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

def test_analytics_growth(run_sql):
    rows = run_sql()
    # Data:
    # 2023-01: 10000 (Lag: null) -> Filtered out
    # 2023-02: 12000 (Lag: 10000) -> Growth: 2000
    # 2023-03: 11000 (Lag: 12000) -> Growth: -1000
    # 2023-04: 15000 (Lag: 11000) -> Growth: 4000
    
    assert len(rows) == 3
    
    # Check growth (4th col, index 3)
    assert rows[0][3] == 2000
    assert rows[1][3] == -1000
    assert rows[2][3] == 4000

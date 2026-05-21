
import unittest
from pathlib import Path
from data._shared.sql_test_helpers import run_sql as base_run_sql

BASE_DIR = Path(__file__).resolve().parent
if (BASE_DIR / "fixtures").exists():
    SCHEMA_SQL = BASE_DIR / "fixtures" / "schema.sql"
    SEED_SQL = BASE_DIR / "fixtures" / "seed.sql"
    TASK_SQL = BASE_DIR / "task.sql"
else:
    QUEST_DIR = BASE_DIR.parents[1]
    TASK_SQL = QUEST_DIR / "workspace" / "task.sql"
    SCHEMA_SQL = QUEST_DIR / "workspace" / "fixtures" / "schema.sql"
    SEED_SQL = QUEST_DIR / "workspace" / "fixtures" / "seed.sql" 
def run_sql():
    return base_run_sql(TASK_SQL, SCHEMA_SQL, SEED_SQL)


class TestTask(unittest.TestCase):
    def test_window_function(self):
        rows = run_sql()
        # Sort by department then rank to verify
        # Engineering: Charlie (95k) -> 1, Alice (90k) -> 2, Bob (80k) -> 3

        
        eng = [r for r in rows if r[1] == 'Engineering']
        eng_sorted = sorted(eng, key=lambda x: x[2], reverse=True) # Sort by salary desc

        
        assert len(eng) == 3
        # Check ranks (4th column, index 3)
        # The output order from query might differ unless ORDER BY is in main query, 
        # but the rank value must match the salary order.

        
        # We expect the query output to have rank calculated correctly.
        # Let's map name to rank
        name_to_rank = {r[0]: r[3] for r in eng}

        
        assert name_to_rank['Charlie'] == 1
        assert name_to_rank['Alice'] == 2
        assert name_to_rank['Bob'] == 3


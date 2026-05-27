
import unittest
from pathlib import Path
# We assume data._shared.sql_test_helpers exists as per sql-ignition reference
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
    def test_groupby_having(self):
        rows = run_sql()
        # Expect only 'Vegetable' (6 items)
        # Fruit has 3, Electronics has 3.
        # We want count > 5.

        
        assert len(rows) == 1
        assert rows[0][0] == 'Vegetable'
        assert rows[0][1] == 6


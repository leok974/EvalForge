
import unittest
from pathlib import Path
from data._shared.sql_test_helpers import run_sql as base_run_sql, assert_rows_match

QUEST_DIR = Path(__file__).resolve().parents[2]
# Using task.sql in workspace (swapped in solution mode)
TASK_SQL = QUEST_DIR / "workspace" / "task.sql"
SCHEMA_SQL = QUEST_DIR / "workspace" / "fixtures" / "schema.sql"
SEED_SQL = QUEST_DIR / "workspace" / "fixtures" / "seed.sql"

def run_sql():
    return base_run_sql(TASK_SQL, SCHEMA_SQL, SEED_SQL)


class TestTask(unittest.TestCase):
    def test_sql_subqueries_exists(self):
        rows = run_sql()
        # 1 (Alice) manages 2
        # 2 (Bob) manages 3
        # 3 (Charlie) manages 4, 5
        assert len(rows) == 3
        assert rows[0] == (1, 'Alice (CEO)')
        assert rows[1] == (2, 'Bob (VP)')
        assert rows[2] == (3, 'Charlie (Manager)')




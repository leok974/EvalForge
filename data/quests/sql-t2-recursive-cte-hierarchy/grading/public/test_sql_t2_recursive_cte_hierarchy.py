
import unittest
from pathlib import Path
from data._shared.sql_test_helpers import run_sql as base_run_sql, assert_rows_match

QUEST_DIR = Path(__file__).resolve().parents[2]
# Using task.sql in workspace (swapped in solution mode)
TASK_SQL = QUEST_DIR / "workspace" / "task.sql"
SCHEMA_SQL = QUEST_DIR / "fixtures" / "schema.sql"
SEED_SQL = QUEST_DIR / "fixtures" / "seed.sql"

def run_sql():
    return base_run_sql(TASK_SQL, SCHEMA_SQL, SEED_SQL)


class TestTask(unittest.TestCase):
    def test_sql_recursive_cte(self):
        rows = run_sql()
        assert len(rows) == 5
        assert rows[0] == (1, 'Alice (CEO)', 0) # Alice
        assert rows[1] == (2, 'Bob (VP)', 1)    # Bob
        assert rows[2] == (3, 'Charlie (Manager)', 2) # Charlie
        assert rows[3] == (4, 'Diana (IC)', 3)  # Diana
        assert rows[4] == (5, 'Evan (IC)', 3)   # Evan




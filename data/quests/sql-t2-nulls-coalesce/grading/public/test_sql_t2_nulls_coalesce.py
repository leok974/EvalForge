
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
    def test_sql_nulls_coalesce(self):
        rows = run_sql()
        assert len(rows) == 5
        assert rows[0] == (1, 'Alice (CEO)', 250000)
        assert rows[1] == (2, 'Bob (VP)', 150000)
        assert rows[2] == (3, 'Charlie (Manager)', 110000)
        assert rows[3] == (4, 'Diana (IC)', 80000)
        assert rows[4] == (5, 'Evan (IC)', 80000)




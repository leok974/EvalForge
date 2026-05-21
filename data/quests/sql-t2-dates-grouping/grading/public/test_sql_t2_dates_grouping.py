
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
    def test_sql_dates_grouping(self):
        rows = run_sql()
        assert len(rows) == 3
        assert rows[0] == ('2023-10-01', 2)
        assert rows[1] == ('2023-10-02', 2)
        assert rows[2] == ('2023-10-03', 2)




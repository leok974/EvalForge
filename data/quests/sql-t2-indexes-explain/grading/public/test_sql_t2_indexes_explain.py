
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
    def test_sql_indexes_explain(self):
        rows = run_sql()
        # In SQLite 3.x, EXPLAIN QUERY PLAN returns rows with columns (id, parent, notused, detail).
        # We want to check that the 'detail' column mentions the index 'idx_emp_mgr'.
        found_index = False
        for r in rows:
            detail = str(r[-1]).upper()
            if "IDX_EMP_MGR" in detail and ("SEARCH" in detail or "INDEX" in detail):
                found_index = True
                break
        assert found_index, f"Query plan did not use idx_emp_mgr! Rows: {rows}"




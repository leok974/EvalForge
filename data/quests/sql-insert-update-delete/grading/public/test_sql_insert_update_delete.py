from __future__ import annotations

import re
import sys
from pathlib import Path

def _shared():
  return Path(__file__).resolve().parents[4] / "_shared"

sys.path.insert(0, str(_shared()))
from sql_test_helpers import build_db, load_text, assert_safe_dml_sql, run_dml_with_final_select, norm_rows  # type: ignore

def _quest_root() -> Path:
  return Path(__file__).resolve().parents[2]

def test_sql_insert_update_delete_requires_keywords_and_correct_result():
  root = _quest_root()
  con = build_db(load_text(root / "fixtures/schema.sql"), load_text(root / "fixtures/seed.sql"))
  try:
    sql = load_text(root / "workspace/query.sql")
    assert_safe_dml_sql(sql)

    # enforce the learning objective: must contain INSERT, UPDATE, DELETE somewhere
    upper = sql.upper()
    assert "INSERT" in upper, "Expected an INSERT statement"
    assert "UPDATE" in upper, "Expected an UPDATE statement"
    assert "DELETE" in upper, "Expected a DELETE statement"

    res = run_dml_with_final_select(con, sql)
  finally:
    con.close()

  assert res.columns == ["id", "title", "status"]
  assert norm_rows(res.rows) == [
    (1, "setup", "todo"),
    (2, "ship", "done"),
    (4, "monitor", "todo"),
  ]

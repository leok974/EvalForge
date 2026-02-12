from __future__ import annotations

import sys
from pathlib import Path

def _shared():
  return Path(__file__).resolve().parents[4] / "_shared"

sys.path.insert(0, str(_shared()))
from sql_test_helpers import build_db, load_text, assert_readonly_sql, run_select, norm_rows  # type: ignore

def _quest_root() -> Path:
  return Path(__file__).resolve().parents[2]

def test_sql_select():
  root = _quest_root()
  con = build_db(load_text(root / "fixtures/schema.sql"), load_text(root / "fixtures/seed.sql"))
  try:
    sql = load_text(root / "workspace/query.sql")
    assert_readonly_sql(sql)
    res = run_select(con, sql)
  finally:
    con.close()

  assert res.columns == ["id", "name", "city"]
  assert norm_rows(res.rows) == [
    (1, "Alice", "Detroit"),
    (2, "Bob", "Austin"),
    (3, "Charlie", "Boston"),
    (4, "Dana", "Denver"),
  ]

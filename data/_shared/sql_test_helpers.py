from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sqlite3
from typing import Any, Iterable

_DISALLOWED_DDL = re.compile(
  r"\b(drop|alter|create|pragma|attach|detach|vacuum|reindex)\b",
  re.IGNORECASE,
)

_DISALLOWED_WRITE = re.compile(
  r"\b(insert|update|delete|replace)\b",
  re.IGNORECASE,
)

def load_text(path: Path) -> str:
  return path.read_text(encoding="utf-8").strip()

def build_db(schema_sql: str, seed_sql: str) -> sqlite3.Connection:
  con = sqlite3.connect(":memory:")
  con.executescript(schema_sql)
  con.executescript(seed_sql)
  return con

@dataclass(frozen=True)
class SqlResult:
  columns: list[str]
  rows: list[tuple[Any, ...]]

def run_select(con: sqlite3.Connection, sql: str) -> SqlResult:
  cur = con.execute(sql)
  cols = [d[0] for d in (cur.description or [])]
  rows = cur.fetchall()
  return SqlResult(columns=cols, rows=rows)

def assert_readonly_sql(sql: str) -> None:
  if _DISALLOWED_DDL.search(sql):
    raise AssertionError("Query contains disallowed DDL keyword (DROP/ALTER/CREATE/PRAGMA/etc).")
  if _DISALLOWED_WRITE.search(sql):
    raise AssertionError("Query must be read-only (SELECT/CTE only). Write keyword found (INSERT/UPDATE/DELETE/etc).")

def assert_safe_dml_sql(sql: str) -> None:
  # For the DML quest: allow INSERT/UPDATE/DELETE/SELECT, but still disallow DDL + PRAGMA/ATTACH/etc.
  if _DISALLOWED_DDL.search(sql):
    raise AssertionError("SQL contains disallowed DDL keyword (DROP/ALTER/CREATE/PRAGMA/etc).")

def norm_rows(rows: Iterable[tuple[Any, ...]]) -> list[tuple[Any, ...]]:
  return [tuple(r) for r in rows]

def split_statements(sql: str) -> list[str]:
  # naive split by ';' (acceptable for our controlled quests: no semicolons in strings)
  parts = [p.strip() for p in sql.strip().split(";")]
  return [p for p in parts if p]

def run_dml_with_final_select(con: sqlite3.Connection, sql: str) -> SqlResult:
  stmts = split_statements(sql)
  if not stmts:
    raise AssertionError("No SQL statements found.")

  for stmt in stmts[:-1]:
    con.execute(stmt)

  last = stmts[-1]
  return run_select(con, last)

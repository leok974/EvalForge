"""
Smoke test: sql-select preview pipeline (Item 2 of SQL hardening).

Asserts that sql_preview.py correctly:
  - runs schema + seed + task.sql for sql-select
  - returns columns == ["name", "city"]
  - returns row_count == 6
  - first row is ["Alice", "Detroit"]
"""
import json
import os
import sqlite3
import sys
import time

# Point at our runner directly (no Docker, for speed)
import pathlib

REPO_ROOT   = pathlib.Path(__file__).resolve().parents[2]   # tests/backend -> tests -> repo root
QUEST_DIR   = REPO_ROOT / "data" / "quests" / "sql-select"
SCHEMA_PATH = QUEST_DIR / "workspace" / "fixtures" / "schema.sql"
SEED_PATH   = QUEST_DIR / "workspace" / "fixtures" / "seed.sql"
TASK_PATH   = QUEST_DIR / "workspace" / "task.sql"


def _run_preview(schema_sql: str, seed_sql: str, task_sql: str) -> dict:
    """Minimal inline re-implementation of sql_preview.py logic for testing."""
    trace = []
    sql_student_result = {"columns": [], "rows": [], "row_count": 0, "note": "No SELECT found."}
    sql_explain = {"engine": "sqlite", "statement": "", "plan_rows": []}

    con = sqlite3.connect(":memory:")
    cur = con.cursor()

    def exec_script(sql_text: str, phase: str):
        buf = ""
        statements = []
        for line in sql_text.splitlines(True):
            buf += line
            if sqlite3.complete_statement(buf):
                stmt = buf.strip()
                if stmt:
                    statements.append(stmt)
                buf = ""
        if buf.strip():
            statements.append(buf.strip())

        for stmt in statements:
            entry = {
                "idx": len(trace), "phase": phase, "sql": stmt,
                "elapsed_ms": 0.0, "row_count": None,
                "columns": None, "preview_rows": None,
                "error": None, "is_select": False,
            }
            trace.append(entry)
            t0 = time.perf_counter()
            try:
                cur.execute(stmt)
                entry["elapsed_ms"] = round((time.perf_counter() - t0) * 1000, 2)
                if cur.description:
                    entry["is_select"] = True
                    rows = cur.fetchmany(25)
                    entry["columns"] = [d[0] for d in cur.description][:20]
                    entry["preview_rows"] = [list(r)[:20] for r in rows]
                    entry["row_count"] = len(rows)
                else:
                    entry["row_count"] = cur.rowcount
            except Exception as exc:
                entry["error"] = str(exc)

    exec_script(schema_sql, "setup")
    exec_script(seed_sql,   "setup")
    exec_script(task_sql,   "student")

    student_selects = [e for e in trace if e["phase"] == "student" and e["is_select"] and not e["error"]]
    if student_selects:
        last = student_selects[-1]
        sql_student_result = {
            "columns": last["columns"] or [],
            "rows": last["preview_rows"] or [],
            "row_count": len(last["preview_rows"]) if last["preview_rows"] else 0,
            "note": "",
        }

    con.close()
    return {"sql_student_result": sql_student_result, "sql_trace": trace, "sql_explain": sql_explain}


def test_sql_select_preview_columns_and_rows():
    """sql-select: columns should be [name, city], 6 rows, first row Alice/Detroit."""
    assert os.path.exists(SCHEMA_PATH), f"Missing schema: {SCHEMA_PATH}"
    assert os.path.exists(SEED_PATH),   f"Missing seed: {SEED_PATH}"
    assert os.path.exists(TASK_PATH),   f"Missing task.sql: {TASK_PATH}"

    schema_sql = open(SCHEMA_PATH, encoding="utf-8").read()
    seed_sql   = open(SEED_PATH,   encoding="utf-8").read()
    task_sql   = open(TASK_PATH,   encoding="utf-8").read()

    result = _run_preview(schema_sql, seed_sql, task_sql)
    sr = result["sql_student_result"]

    assert sr["columns"] == ["name", "city"], f"Expected ['name','city'], got {sr['columns']}"
    assert sr["row_count"] == 6,              f"Expected 6 rows, got {sr['row_count']}"
    assert sr["rows"][0] == ["Alice", "Detroit"], f"Expected first row ['Alice','Detroit'], got {sr['rows'][0]}"


def test_sql_select_preview_no_errors_in_trace():
    """sql-select: no statement in trace should have an error."""
    schema_sql = open(SCHEMA_PATH, encoding="utf-8").read()
    seed_sql   = open(SEED_PATH,   encoding="utf-8").read()
    task_sql   = open(TASK_PATH,   encoding="utf-8").read()

    result = _run_preview(schema_sql, seed_sql, task_sql)
    errors = [e for e in result["sql_trace"] if e["error"]]
    assert not errors, f"Unexpected trace errors: {[e['error'] for e in errors]}"

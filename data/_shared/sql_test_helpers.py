
import sqlite3
from pathlib import Path

import json
import time
import os

MAX_TRACE_ENTRIES = 200
MAX_SQL_CHARS = 4000
MAX_PREVIEW_ROWS = 25
MAX_PREVIEW_COLS = 20
MAX_CELL_CHARS = 200

def split_statements(sql_text: str) -> list[str]:
    statements = []
    buf = ""
    for line in sql_text.splitlines(True):
        buf += line
        if sqlite3.complete_statement(buf):
            stmt = buf.strip()
            if stmt:
                statements.append(stmt)
            buf = ""
    # Add any remaining complete statement (or incomplete if at EOF)
    if buf.strip():
        statements.append(buf.strip())
    return statements

def safe_str(val) -> str:
    if val is None:
        return None
    if isinstance(val, (int, float, bool)):
        return val
    s = str(val)
    if len(s) > MAX_CELL_CHARS:
        return s[:MAX_CELL_CHARS] + "..."
    return s

def execute_sql_script(cur: sqlite3.Cursor, sql_text: str, phase: str, trace: list) -> list[tuple]:
    statements = split_statements(sql_text)
    last_rows = []
    
    for stmt in statements:
        if len(trace) >= MAX_TRACE_ENTRIES:
            break
            
        entry = {
            "idx": len(trace),
            "phase": phase,
            "sql": stmt if len(stmt) <= MAX_SQL_CHARS else stmt[:MAX_SQL_CHARS] + "...",
            "elapsed_ms": 0.0,
            "row_count": None,
            "columns": None,
            "preview_rows": None,
            "error": None,
            "is_select": False
        }
        trace.append(entry)
        
        stmt_upper = stmt.lstrip().upper()
        is_select = (
            stmt_upper.startswith("SELECT") or 
            stmt_upper.startswith("WITH") or 
            stmt_upper.startswith("PRAGMA") or 
            stmt_upper.startswith("EXPLAIN") or 
            " RETURNING " in stmt_upper
        )
        entry["is_select"] = is_select
        
        t0 = time.perf_counter()
        try:
            cur.execute(stmt)
            entry["elapsed_ms"] = round((time.perf_counter() - t0) * 1000, 2)
            
            if is_select:
                rows = cur.fetchmany(MAX_PREVIEW_ROWS)
                last_rows = rows # For return value
                if cur.description:
                    entry["columns"] = [d[0] for d in cur.description][:MAX_PREVIEW_COLS]
                    entry["preview_rows"] = [
                        [safe_str(x) for x in list(row)[:MAX_PREVIEW_COLS]] 
                        for row in rows
                    ]
                    # We fetched up to MAX_PREVIEW_ROWS, row_count is at least this.
                    entry["row_count"] = len(rows) 
            else:
                entry["row_count"] = cur.rowcount
                last_rows = []
                
        except Exception as e:
            entry["elapsed_ms"] = round((time.perf_counter() - t0) * 1000, 2)
            entry["error"] = f"{type(e).__name__}: {str(e)}"
            raise
            
    return last_rows

def run_sql(task_sql_path: Path | str, schema_sql_path: Path | str, seed_sql_path: Path | str) -> list[tuple]:
    """
    Runs schema -> seed -> task in an in-memory SQLite DB with execution tracing.
    Returns list of tuples (rows) for the last statement in the task sequence.
    """
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    
    trace = []
    sql_student_result = None
    sql_explain = None
    
    try:
        # Load Schema
        with open(schema_sql_path, "r", encoding="utf-8") as f:
            execute_sql_script(cur, f.read(), "setup", trace)

        # Load Seed
        with open(seed_sql_path, "r", encoding="utf-8") as f:
            execute_sql_script(cur, f.read(), "setup", trace)

        # Run Task
        with open(task_sql_path, "r", encoding="utf-8") as f:
            task_sql = f.read()

        rows = execute_sql_script(cur, task_sql, "student", trace)
        
        # Capture student result and explain
        # Find the first student select (or the last if multiple, we'll use the last select)
        student_selects = [e for e in trace if e["phase"] == "student" and e["is_select"] and not e["error"]]
        if student_selects:
            student_stmt = student_selects[-1]
            sql_student_result = {
                "columns": student_stmt["columns"],
                "preview_rows": student_stmt["preview_rows"],
                "row_count_preview": len(student_stmt["preview_rows"]) if student_stmt["preview_rows"] else 0,
                "note": f"Preview limited to {MAX_PREVIEW_ROWS} rows and {MAX_PREVIEW_COLS} columns"
            }
            
            # Explain
            try:
                cur.execute(f"EXPLAIN QUERY PLAN {student_stmt['sql']}")
                plan_rows = [str(r) for r in cur.fetchall()]
                sql_explain = {
                    "engine": "sqlite",
                    "statement": student_stmt["sql"],
                    "plan_rows": plan_rows
                }
            except Exception:
                pass
                
        return rows
        
    finally:
        con.close()
        
        # Write artifacts safely
        try:
            cwd = Path(os.getenv("EF_ARTIFACTS_DIR", os.getcwd()))
            with open(cwd / "sql_trace.json", "w", encoding="utf-8") as f:
                json.dump(trace, f)
                
            if sql_student_result:
                with open(cwd / "sql_student_result.json", "w", encoding="utf-8") as f:
                    json.dump(sql_student_result, f)
                    
            if sql_explain:
                with open(cwd / "sql_explain.json", "w", encoding="utf-8") as f:
                    json.dump(sql_explain, f)
        except Exception as e:
            # If the artifact directory is read-only or missing (e.g. strict Docker modes), fail gracefully
            import sys
            print(f"Warning: Could not write SQL artifacts to disk: {e}", file=sys.stderr)

def assert_rows_match(actual, expected, order_matters=True):
    """
    Asserts that actual rows match expected rows.
    If order_matters is False, both are sorted before comparison.
    """
    assert len(actual) == len(expected), f"Row count mismatch: expected {len(expected)}, got {len(actual)}"
    
    if not order_matters:
        actual = sorted(actual)
        expected = sorted(expected)
    
    assert actual == expected, f"Rows mismatch.\nExpected:\n{expected}\nActual:\n{actual}"

def normalize_rows(rows):
    """Helper to maybe round floats or normalize strings if needed."""
    return rows

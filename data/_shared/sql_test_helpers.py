
import sqlite3
import pytest
from pathlib import Path

def run_sql(task_sql_path: Path | str, schema_sql_path: Path | str, seed_sql_path: Path | str) -> list[tuple]:
    """
    Runs schema -> seed -> task in an in-memory SQLite DB.
    Returns list of tuples (rows).
    """
    con = sqlite3.connect(":memory:")
    cur = con.cursor()

    # Load Schema
    with open(schema_sql_path, "r", encoding="utf-8") as f:
        cur.executescript(f.read())

    # Load Seed
    with open(seed_sql_path, "r", encoding="utf-8") as f:
        cur.executescript(f.read())

    # Run Task
    with open(task_sql_path, "r", encoding="utf-8") as f:
        script = f.read()
    
    # We allow multiple statements (for DML), but we return the result of the *last* statement if it's a SELECT.
    # To do this robustly with sqlite3, we can use executescript but it doesn't return rows.
    # So we split by ';', execute non-selects, then execute the final select?
    # Or just use executescript for everything setup, then execute the student query.
    # The student query might be multiple statements (INSERT...; SELECT...).
    
    # Strategy: split script by semicolon, execute all but last. Execute last and fetch.
    # This is brittle if semicolons are in strings, but for this level it's fine.
    # BETTER: Use executescript() then try to fetch results? executescript return None.
    
    # Alternative: The student task might contain multiple queries. We expect the *last* one to be the answer.
    # But sqlite3 python api is tricky with multiple statements.
    
    try:
        # Re-approach:
        # 1. Split script into statements.
        statements = [s.strip() for s in script.split(";") if s.strip()]
        if not statements:
            return []
            
        # Execute all but the last one
        for i, stmt in enumerate(statements[:-1]):
            # print(f"EXEC {i}: {stmt[:50]}...")
            cur.execute(stmt)
            
        # Execute the last one and fetch
        last = statements[-1]
        # print(f"EXEC LAST: {last[:50]}...")
        if last.upper().startswith("SELECT") or last.upper().startswith("WITH") or "SELECT" in last.upper():
             cur.execute(last)
             rows = cur.fetchall()
             # print(f"ROWS: {len(rows)}")
             return rows
        else:
             # If last statement is not a SELECT, just execute it and return empty
             cur.execute(last)
             return []
        
    except sqlite3.Error as e:
        # Fallback debug or just raise
        raise RuntimeError(f"SQL Error: {e}") from e
    finally:
        con.close()

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

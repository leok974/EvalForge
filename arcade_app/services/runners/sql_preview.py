import json
import sys
import os
import sqlite3
import time

def main():
    start_dir = '/workspace'
    task_sql_name = os.getenv("EVALFORGE_SQL_ENTRYPOINT", "task.sql")
    task_sql_path = os.path.join(start_dir, task_sql_name)
    schema_sql_path = os.path.join(start_dir, "fixtures", "schema.sql")
    seed_sql_path = os.path.join(start_dir, "fixtures", "seed.sql")

    artifacts_dir = os.getenv("EVALFORGE_ARTIFACTS_DIR", os.path.join(start_dir, ".evalforge"))

    print("INFO[sql-preview] active (Run Mode) — executing fixtures + task.sql", file=sys.stdout)

    trace = []
    sql_student_result = {"columns": [], "rows": [], "row_count": 0, "note": "No valid SELECT statement found."}
    sql_explain = {"engine": "sqlite", "statement": "", "plan_rows": []}

    try:
        con = sqlite3.connect(":memory:")
        cur = con.cursor()

        def execute_sql_script(sql_text, phase):
            statements = []
            buf = ""
            for line in sql_text.splitlines(True):
                buf += line
                if sqlite3.complete_statement(buf):
                    stmt = buf.strip()
                    if stmt: statements.append(stmt)
                    buf = ""
            if buf.strip(): statements.append(buf.strip())
            
            for stmt in statements:
                if len(trace) >= 200: break
                entry = {"idx": len(trace), "phase": phase, "sql": stmt[:4000], "elapsed_ms": 0.0, "row_count": None, "columns": None, "preview_rows": None, "error": None, "is_select": False}
                trace.append(entry)
                
                t0 = time.perf_counter()
                try:
                    cur.execute(stmt)
                    entry["elapsed_ms"] = round((time.perf_counter() - t0) * 1000, 2)
                    
                    if cur.description:
                        entry["is_select"] = True
                        rows = cur.fetchmany(25)
                        entry["columns"] = [d[0] for d in cur.description][:20]
                        entry["preview_rows"] = [[str(x)[:200] if x is not None else None for x in list(row)[:20]] for row in rows]
                        entry["row_count"] = len(rows)
                    else:
                        entry["row_count"] = cur.rowcount
                        
                except Exception as e:
                    entry["elapsed_ms"] = round((time.perf_counter() - t0) * 1000, 2)
                    entry["error"] = f"{type(e).__name__}: {str(e)}"
                    print(f"SQL Error in {phase}: {e}", file=sys.stderr)

        if os.path.exists(schema_sql_path):
            with open(schema_sql_path, "r", encoding="utf-8") as f: execute_sql_script(f.read(), "setup")
        if os.path.exists(seed_sql_path):
            with open(seed_sql_path, "r", encoding="utf-8") as f: execute_sql_script(f.read(), "setup")
            
        if os.path.exists(task_sql_path):
            with open(task_sql_path, "r", encoding="utf-8") as f: execute_sql_script(f.read(), "student")
        else:
            print(f"WARN[sql-preview]: task.sql not found at {task_sql_path}", file=sys.stderr)

        student_selects = [e for e in trace if e["phase"] == "student" and e["is_select"] and not e["error"]]
        if student_selects:
            student_stmt = student_selects[-1]
            sql_student_result = {
                "columns": student_stmt["columns"] or [],
                "rows": student_stmt["preview_rows"] or [],
                "row_count": len(student_stmt["preview_rows"]) if student_stmt["preview_rows"] else 0,
                "note": "Preview limited to 25 rows and 20 columns" if student_stmt["preview_rows"] and len(student_stmt["preview_rows"]) == 25 else ""
            }
            try:
                cur.execute(f"EXPLAIN QUERY PLAN {student_stmt['sql']}")
                sql_explain = {"engine": "sqlite", "statement": student_stmt["sql"], "plan_rows": [str(r) for r in cur.fetchall()]}
            except Exception: pass
        else:
            student_errors = [e for e in trace if e["phase"] == "student" and e["error"]]
            if student_errors:
                last_error = student_errors[-1]["error"]
                print(f"ERROR[sql-preview]: {last_error}", file=sys.stderr)
                sql_student_result["note"] = f"sql_preview error: {last_error}"
    except Exception as e:
        print(f"FATAL[sql-preview]: Error executing SQL logic: {e}", file=sys.stderr)
        sql_student_result["note"] = f"FATAL[sql_preview]: Error executing SQL logic: {e}"
    finally:
        try:
            con.close()
        except Exception:
            pass
        try:
            payload = {
                "sql_trace": trace,
                "sql_student_result": sql_student_result,
                "sql_explain": sql_explain
            }
            print(f"\n<<EVALFORGE_ARTIFACTS_START>>{json.dumps(payload)}<<EVALFORGE_ARTIFACTS_END>>\n")
        except Exception as e:
            print(f"WARN[sql-preview]: Failed to serialize artifacts to stdout: {e}", file=sys.stderr)
            
        written = []
        os.makedirs(artifacts_dir, exist_ok=True)
        for n, d in [("sql_trace", trace), ("sql_student_result", sql_student_result), ("sql_explain", sql_explain)]:
            try:
                p = os.path.join(artifacts_dir, f"{n}.json")
                with open(p, "w", encoding="utf-8") as f: json.dump(d, f)
                written.append(f"{n}.json")
            except Exception as e: 
                print(f"WARN[sql-preview]: Failed writing {n}.json to {artifacts_dir}: {e}", file=sys.stderr)
        print(f"INFO[sql-preview] Artifacts written: {written}", file=sys.stdout)

if __name__ == "__main__":
    main()

import json
import sys
import os
import time
import psycopg2
from psycopg2 import sql

def main():
    start_dir = '/workspace'
    task_sql_path = os.path.join(start_dir, "task.sql")
    schema_sql_path = os.path.join(start_dir, "fixtures", "schema.sql")
    seed_sql_path = os.path.join(start_dir, "fixtures", "seed.sql")

    artifacts_dir = os.getenv("EVALFORGE_ARTIFACTS_DIR", os.path.join(start_dir, ".evalforge"))
    
    # DB Config from Env (Passed by code_runner_docker)
    db_url = os.getenv("PG_DB_URL", "host=db dbname=evalforge user=evalforge password=evalforge")
    temp_schema = os.getenv("PG_TEMP_SCHEMA", f"run_{int(time.time())}")

    print(f"INFO[postgres-preview] active — schema: {temp_schema}", file=sys.stdout)

    trace = []
    sql_student_result = {"columns": [], "rows": [], "row_count": 0, "note": "No valid SELECT statement found."}
    sql_explain = {"engine": "postgres", "statement": "", "plan_rows": []}

    con = None
    try:
        con = psycopg2.connect(db_url)
        con.autocommit = True
        cur = con.cursor()

        # 1. Setup Isolated Schema
        cur.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(temp_schema)))
        cur.execute(sql.SQL("SET search_path TO {}, public").format(sql.Identifier(temp_schema)))

        def execute_sql_text(sql_text, phase):
            # Simple splits for now, psycopg2 doesn't have a direct 'complete_statement' helper like sqlite
            # We'll split by semicolon and filter empty.
            statements = [s.strip() for s in sql_text.split(";") if s.strip()]
            
            for stmt in statements:
                if len(trace) >= 200: break
                entry = {
                    "idx": len(trace), 
                    "phase": phase, 
                    "sql": stmt[:4000], 
                    "elapsed_ms": 0.0, 
                    "row_count": None, 
                    "columns": None, 
                    "preview_rows": None, 
                    "error": None, 
                    "is_select": False
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
                        # PostgreSQL returns real types, normalize to strings for artifact consistency
                        entry["preview_rows"] = [[str(x) if x is not None else None for x in list(row)[:20]] for row in rows]
                        entry["row_count"] = len(rows)
                    else:
                        entry["row_count"] = cur.rowcount
                        
                except Exception as e:
                    entry["elapsed_ms"] = round((time.perf_counter() - t0) * 1000, 2)
                    entry["error"] = f"{type(e).__name__}: {str(e)}"
                    print(f"SQL Error in {phase}: {e}", file=sys.stderr)

        # 2. Execute Fixtures
        if os.path.exists(schema_sql_path):
            with open(schema_sql_path, "r", encoding="utf-8") as f: execute_sql_text(f.read(), "setup")
        if os.path.exists(seed_sql_path):
            with open(seed_sql_path, "r", encoding="utf-8") as f: execute_sql_text(f.read(), "setup")
            
        # 3. Execute Student Task
        if os.path.exists(task_sql_path):
            with open(task_sql_path, "r", encoding="utf-8") as f: execute_sql_text(f.read(), "student")

        # 4. Resolve Artifacts
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
                # Optimized for Postgres
                cur.execute(f"EXPLAIN {student_stmt['sql']}")
                sql_explain = {"engine": "postgres", "statement": student_stmt["sql"], "plan_rows": [str(r[0]) for r in cur.fetchall()]}
            except Exception: pass
        else:
            student_errors = [e for e in trace if e["phase"] == "student" and e["error"]]
            if student_errors:
                sql_student_result["note"] = f"postgres_preview error: {student_errors[-1]['error']}"

    except Exception as e:
        print(f"FATAL[postgres-preview]: {e}", file=sys.stderr)
        sql_student_result["note"] = f"FATAL[postgres_preview]: {e}"
    finally:
        if con:
            try:
                # Cleanup schema? Usually we want to keep it per-run for inspection? 
                # For Phase 1, we leave it or clean it. 
                # Instructions say "schema isolation strategy", usually temp is better.
                # cur.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(temp_schema)))
                con.close()
            except Exception: pass

        # Artifact Serialization (identical to sql_preview.py)
        payload = {"sql_trace": trace, "sql_student_result": sql_student_result, "sql_explain": sql_explain}
        print(f"\n<<EVALFORGE_ARTIFACTS_START>>{json.dumps(payload)}<<EVALFORGE_ARTIFACTS_END>>\n")
        
        os.makedirs(artifacts_dir, exist_ok=True)
        for n, d in [("sql_trace", trace), ("sql_student_result", sql_student_result), ("sql_explain", sql_explain)]:
            try:
                with open(os.path.join(artifacts_dir, f"{n}.json"), "w", encoding="utf-8") as f: json.dump(d, f)
            except Exception: pass

if __name__ == "__main__":
    main()

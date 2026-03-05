import pytest
import tempfile
import json
import os
from pathlib import Path
from data._shared.sql_test_helpers import run_sql

def test_sql_tracer_success():
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        
        schema = tdp / "schema.sql"
        schema.write_text("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);")
        
        seed = tdp / "seed.sql"
        seed.write_text("INSERT INTO users (name) VALUES ('Alice');\nINSERT INTO users (name) VALUES ('Bob');")
        
        task = tdp / "task.sql"
        task.write_text("SELECT * FROM users WHERE name = 'Alice';")
        
        # Override artifacts dir
        os.environ["EF_ARTIFACTS_DIR"] = td
        
        rows = run_sql(task, schema, seed)
        
        assert len(rows) == 1
        assert rows[0][1] == 'Alice'
        
        # Check artifacts
        trace_path = tdp / "sql_trace.json"
        assert trace_path.exists()
        
        with open(trace_path) as f:
            trace = json.load(f)
            
        assert len(trace) >= 3 # schema, seed, task
        
        student_trace = [t for t in trace if t["phase"] == "student"]
        assert len(student_trace) == 1
        assert student_trace[0]["is_select"] is True
        assert student_trace[0]["row_count"] == 1
        assert student_trace[0]["preview_rows"] == [[1, "Alice"]]
        assert student_trace[0]["columns"] == ["id", "name"]
        
        student_res_path = tdp / "sql_student_result.json"
        assert student_res_path.exists()
        with open(student_res_path) as f:
            res = json.load(f)
            assert res["row_count_preview"] == 1
            assert res["columns"] == ["id", "name"]
            
        explain_path = tdp / "sql_explain.json"
        assert explain_path.exists()
        with open(explain_path) as f:
            expl = json.load(f)
            assert expl["statement"] == "SELECT * FROM users WHERE name = 'Alice';"
            assert len(expl["plan_rows"]) > 0

def test_sql_tracer_failure():
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        
        schema = tdp / "schema.sql"
        schema.write_text("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);")
        
        seed = tdp / "seed.sql"
        seed.write_text("INSERT INTO users (name) VALUES ('Alice');")
        
        task = tdp / "task.sql"
        task.write_text("SELECT * FROM fake_table;")
        
        # Override artifacts dir
        os.environ["EF_ARTIFACTS_DIR"] = td
        
        with pytest.raises(Exception) as exc:
            run_sql(task, schema, seed)
            
        assert "no such table: fake_table" in str(exc.value)
        
        # Check artifacts
        trace_path = tdp / "sql_trace.json"
        assert trace_path.exists()
        
        with open(trace_path) as f:
            trace = json.load(f)
            
        student_trace = [t for t in trace if t["phase"] == "student"]
        assert len(student_trace) == 1
        assert student_trace[0]["error"] is not None
        assert "no such table" in student_trace[0]["error"]

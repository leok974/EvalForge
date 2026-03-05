import pytest
from arcade_app.services.utils import build_effective_workspace

def test_normalization_dict_to_list():
    base = {
        "files": {
            "task.sql": "SELECT 1;"
        }
    }
    overlay = {
        "task.sql": "SELECT 2;"
    }
    
    # build_effective_workspace should handle dicts
    result = build_effective_workspace(base, overlay)
    files = result.get("files", [])
    assert isinstance(files, list)
    assert len(files) == 1
    assert files[0]["path"] == "task.sql"
    assert files[0]["content"] == "SELECT 2;"

def test_normalization_list_to_list():
    base = {
        "files": [
            {"path": "test_task.py", "content": "print('hello')", "editable": False}
        ]
    }
    overlay = [
        {"path": "test_task.py", "content": "print('hacked')"}
    ]
    
    result = build_effective_workspace(base, overlay)
    files = result.get("files", [])
    assert files[0]["content"] == "print('hello')" # not editable

def test_sql_workspace_injection_basic():
    from arcade_app.services.utils import inject_sql_task
    
    workspace = {"files": [{"path": "other.py", "content": "print()"}]}
    code = "SELECT * FROM heroes;"
    
    result = inject_sql_task(workspace, code)
    files = result["files"]
    assert len(files) == 2
    assert result["entrypoint"] == "task.sql"
    # Ensure it's exactly task.sql
    assert any(f["path"] == "task.sql" and f["content"] == code for f in files)

def test_sql_workspace_injection_override():
    from arcade_app.services.utils import inject_sql_task
    
    workspace = {
        "files": [
            {"path": "task.sql", "content": "BAD_SQL"},
            {"path": "workspace/task.sql", "content": "BAD_SQL_2"}
        ]
    }
    code = "SELECT 1;"
    
    result = inject_sql_task(workspace, code)
    files = result["files"]
    assert len(files) == 1
    assert files[0]["path"] == "task.sql"
    assert files[0]["content"] == code

def test_sql_workspace_injection_empty():
    from arcade_app.services.utils import inject_sql_task
    
    workspace = None
    code = "SELECT 2;"
    
    result = inject_sql_task(workspace, code)
    assert len(result["files"]) == 1
    assert result["files"][0]["path"] == "task.sql"
    assert result["files"][0]["content"] == code

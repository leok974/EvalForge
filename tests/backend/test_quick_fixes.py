import pytest
from arcade_app.services.quick_fix_generator import generate_quick_fixes

def test_quick_fix_tabs_to_spaces():
    """Verify tabs-to-spaces fix is generated for IndentationError."""
    diagnostics = [{
        "path": "main.py",
        "line": 2,
        "column": 1,
        "message": "IndentationError: unexpected indent",
        "kind": "runtime"
    }]
    workspace = {
        "main.py": {"content": "def foo():\n\treturn 1"}
    }
    
    fixes = generate_quick_fixes("python", None, diagnostics, [], workspace)
    
    assert len(fixes) > 0
    fix = next((f for f in fixes if f.id == "fix-tabs-to-spaces"), None)
    assert fix is not None
    assert fix.kind == "apply_patch"
    assert "Convert tabs" in fix.title
    assert fix.patch["path"] == "main.py"
    assert fix.patch["replacement_full_content"] == "def foo():\n    return 1"

def test_quick_fix_output_mismatch():
    """Verify output mismatch generates print snippet."""
    objectives = [{
        "kind": "stdout_regex",
        "ok": False,
        "detail": "Expected matches: Hello"
    }]
    
    fixes = generate_quick_fixes("python", None, [], objectives, {})
    
    assert len(fixes) > 0
    fix = next((f for f in fixes if f.id == "fix-output-mismatch"), None)
    assert fix is not None
    assert fix.kind == "copy_snippet"
    assert 'print("Expected Output")' in fix.snippet

def test_quick_fix_hidden_tests_no_leakage():
    """Verify hidden test failure does not leak info."""
    failure = {"primary_failure": {"kind": "hidden_tests_failed"}}
    
    fixes = generate_quick_fixes("python", failure, [], [], {}, hidden_tests_reveal=False)
    
    assert len(fixes) > 0
    fix = next((f for f in fixes if f.id == "fix-check-edge-cases"), None)
    assert fix is not None
    assert fix.kind == "copy_snippet" # It's a comment snippet
    assert "# Checklist" in fix.snippet
    # Ensure no file paths or names
    assert "test_hidden.py" not in fix.snippet

def test_quick_fix_navigate():
    """Verify generic navigation fix if diagnostics exist."""
    diagnostics = [{
        "path": "main.py",
        "line": 10,
        "column": 5,
        "message": "SyntaxError",
        "kind": "syntax"
    }]
    
    fixes = generate_quick_fixes("python", None, diagnostics, [], {})
    
    # Might have tab fix too if unlucky, but navigate should be there
    fix = next((f for f in fixes if f.kind == "navigate"), None)
    assert fix is not None
    assert fix.locator["line"] == 10

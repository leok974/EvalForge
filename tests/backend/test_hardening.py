
import pytest
from arcade_app.services.security import safe_relpath, sanitize_logs, validate_workspace_limits
from arcade_app.services.utils import build_effective_workspace

def test_safe_relpath_valid():
    assert safe_relpath("foo.py") == "foo.py"
    assert safe_relpath("dir/foo.py") == "dir/foo.py"
    
def test_safe_relpath_traversal():
    with pytest.raises(ValueError, match="Path traversal"):
        safe_relpath("../foo.py")
        
    with pytest.raises(ValueError, match="Path traversal"):
        safe_relpath("dir/../../foo.py")
        
def test_safe_relpath_absolute():
    with pytest.raises(ValueError, match="relative"):
        safe_relpath("/etc/passwd")
        
def test_safe_relpath_chars():
    with pytest.raises(ValueError, match="invalid characters"):
        safe_relpath("foo*.py")

def test_sanitize_logs():
    assert sanitize_logs("Hello World") == "Hello World"
    # Test path stripping
    assert sanitize_logs("Error in /workspace/main.py") == "Error in main.py"
    assert sanitize_logs("Traceback (most recent call last):\n  File \"/tmp/execution/test.py\", line 1") == "Traceback (most recent call last):\n  File \"execution/test.py\", line 1"
    
    # Test windows path (partial check as it's regex based)
    assert sanitize_logs(r"Error in D:\EvalForge\main.py") == "Error in main.py"

def test_build_effective_workspace():
    base = {
        "files": [
            {"path": "main.py", "content": "print(1)", "editable": True},
            {"path": "readonly.py", "content": "secret", "editable": False}
        ]
    }
    
    # 1. Valid Overlay
    overlay = [{"path": "main.py", "content": "print(2)"}]
    eff = build_effective_workspace(base, overlay)
    files = {f["path"]: f for f in eff["files"]}
    
    assert files["main.py"]["content"] == "print(2)"
    assert files["readonly.py"]["content"] == "secret"
    
    # 2. Ignored Overlay (Read-only)
    overlay = [{"path": "readonly.py", "content": "hacked"}]
    eff = build_effective_workspace(base, overlay)
    files = {f["path"]: f for f in eff["files"]}
    assert files["readonly.py"]["content"] == "secret" # Should not change
    
    # 3. Ignored Overlay (New file not allowed)
    overlay = [{"path": "new.py", "content": "hacked"}]
    eff = build_effective_workspace(base, overlay)
    files = {f["path"]: f for f in eff["files"]}
    assert "new.py" not in files

def test_workspace_limits():
    # Test max files
    files = [{"path": f"f{i}.py", "content": ""} for i in range(101)] # Assuming 64 limit
    # The actual limit is defined in security.py, let's assume it's small or verify
    # If limit is 64, 101 should fail.
    
    with pytest.raises(ValueError, match="Too many files"):
        validate_workspace_limits(files)
        
    # Test max size
    files = [{"path": "biig.py", "content": "a" * (1024 * 1024 + 1)}] # 1MB limit per file?
    with pytest.raises(ValueError, match="too large"):
        validate_workspace_limits(files)

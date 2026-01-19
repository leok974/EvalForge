import sys
from arcade_app.services.diagnostics_parser import parse_diagnostics

def test_parse_python_traceback():
    stderr = """Traceback (most recent call last):
  File "src/main.py", line 12, in <module>
    print(add(1, 2))
  File "src/main.py", line 5, in add
    return x / 0
ZeroDivisionError: division by zero
"""
    files = ["src/main.py"]
    diags = parse_diagnostics(stderr, "python", files)
    assert len(diags) == 1
    assert diags[0]["path"] == "src/main.py"
    assert diags[0]["line"] == 5
    assert diags[0]["kind"] == "runtime"
    assert "ZeroDivisionError" in diags[0]["message"]
    print("test_parse_python_traceback passed")

def test_parse_python_syntax_error():
    stderr = """  File "src/main.py", line 10
    if True
          ^
SyntaxError: expected ':'
"""
    files = ["src/main.py"]
    diags = parse_diagnostics(stderr, "python", files)
    assert len(diags) == 1
    assert diags[0]["path"] == "src/main.py"
    assert diags[0]["line"] == 10
    assert diags[0]["kind"] == "syntax"
    assert "SyntaxError" in diags[0]["message"]
    print("test_parse_python_syntax_error passed")

def test_parse_ts_error():
    stderr = """src/main.ts:12:5: error: Unexpected token ')'
    at /workspace/src/main.ts:12:5
"""
    files = ["src/main.ts"]
    diags = parse_diagnostics(stderr, "typescript", files)
    assert len(diags) >= 1
    d = diags[0]
    assert d["path"] == "src/main.ts"
    assert d["line"] == 12
    assert d["column"] == 5
    assert "Unexpected token" in d["message"]
    print("test_parse_ts_error passed")

def test_workspace_filtering():
    stderr = """  File "/usr/lib/python3.9/threading.py", line 973, in _bootstrap
    self._bootstrap_inner()
  File "src/main.py", line 5, in <module>
    raise ValueError("oops")
ValueError: oops
"""
    files = ["src/main.py"] 
    diags = parse_diagnostics(stderr, "python", files)
    assert len(diags) == 1
    assert diags[0]["path"] == "src/main.py"
    print("test_workspace_filtering passed")

if __name__ == "__main__":
    try:
        test_parse_python_traceback()
        test_parse_python_syntax_error()
        test_parse_ts_error()
        test_workspace_filtering()
        print("All tests passed")
    except AssertionError as e:
        print(f"Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

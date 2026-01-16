import pytest
from arcade_app.services.code_runner import run_python_local

def test_exec_captures_stdout():
    r = run_python_local("print('Hello World')", timeout_ms=1000)
    assert r.ok
    assert "Hello World" in r.stdout
    assert r.exit_code == 0
    assert not r.timed_out

def test_exec_captures_stderr():
    r = run_python_local("import sys; sys.stderr.write('Error Log')", timeout_ms=1000)
    assert r.ok
    assert "Error Log" in r.stderr

def test_exec_timeout():
    # Infinite loop
    r = run_python_local("while True: pass", timeout_ms=200)
    assert not r.ok
    assert r.timed_out
    assert "[Timed out]" in r.stderr

def test_exec_syntax_error():
    r = run_python_local("print('unclosed string", timeout_ms=1000)
    assert not r.ok
    assert r.exit_code != 0
    assert "SyntaxError" in r.stderr

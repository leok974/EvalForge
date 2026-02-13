import sys
import pytest
from io import StringIO
import importlib.util

def test_stdout_contains_hello_world(capsys):
    # Run the student's script
    # Runner execs in the workspace root, so main.py is in CWD
    spec = importlib.util.spec_from_file_location("main", "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    captured = capsys.readouterr()
    assert "Hello, World!" in captured.out
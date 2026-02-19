import pytest
import sys
from unittest.mock import patch
from task import main

def test_default_args(capsys):
    with patch.object(sys, 'argv', ['prog']):
        main()
    captured = capsys.readouterr()
    assert "Hello World" in captured.out
    assert captured.out.count("Hello World") == 1

def test_count_3(capsys):
    with patch.object(sys, 'argv', ['prog', '--count', '3']):
        main()
    captured = capsys.readouterr()
    assert captured.out.count("Hello World") == 3

def test_verbose(capsys):
    with patch.object(sys, 'argv', ['prog', '--verbose', '--count', '1']):
        main()
    captured = capsys.readouterr()
    assert "Processing 1/1..." in captured.out

def test_negative_count(capsys):
    with patch.object(sys, 'argv', ['prog', '--count', '-1']):
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1
    captured = capsys.readouterr()
    assert "Count cannot be negative" in captured.err

def test_help(capsys):
    with patch.object(sys, 'argv', ['prog', '--help']):
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
    captured = capsys.readouterr()
    assert "usage:" in captured.out

import pytest
from task import read_config
import os

def test_read_valid_config(capsys):
    # Setup
    with open("temp_config.txt", "w") as f:
        f.write("host=127.0.0.1\nport=9000\n")
    
    try:
        res = read_config("temp_config.txt")
        assert res["host"] == "127.0.0.1"
        assert res["port"] == "9000"
    finally:
        os.remove("temp_config.txt")

def test_missing_config(capsys):
    res = read_config("non_existent_file.cfg")
    assert res == {}
    captured = capsys.readouterr()
    assert "CONFIG_MISSING" in captured.out

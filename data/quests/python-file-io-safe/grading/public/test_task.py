import pytest
from task import read_config


def test_read_valid_config(tmp_path, capsys):
    cfg = tmp_path / "config.txt"
    cfg.write_text("host=127.0.0.1\nport=9000\n")
    res = read_config(str(cfg))
    assert res["host"] == "127.0.0.1"
    assert res["port"] == "9000"


def test_missing_config(capsys):
    res = read_config("/tmp/non_existent_file_evalforge.cfg")
    assert res == {}
    captured = capsys.readouterr()
    assert "CONFIG_MISSING" in captured.out

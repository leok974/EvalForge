import sys
from pathlib import Path

QUEST = Path(__file__).resolve().parents[2]
WS = QUEST / "workspace"
sys.path.insert(0, str(WS))

import main  # noqa

def test_verify_output():
    out = main.verify_output({"a":1}, ["a","b"])
    assert out["ok"] is False
    assert out["missing"] == ["b"]

    out2 = main.verify_output({"a":1,"b":2}, ["a","b"])
    assert out2["ok"] is True
    assert out2["missing"] == []

import sys
from pathlib import Path

QUEST = Path(__file__).resolve().parents[2]
WS = QUEST / "workspace"
sys.path.insert(0, str(WS))

import main  # noqa

def test_plan_add():
    p = main.plan("add 2 3", ["add", "echo"])
    assert p == [{"tool":"add","args":{"a":2,"b":3}}]

def test_plan_missing_tool():
    try:
        main.plan("add 1 2", ["echo"])
        assert False
    except ValueError as e:
        assert str(e) == "NO_TOOL"

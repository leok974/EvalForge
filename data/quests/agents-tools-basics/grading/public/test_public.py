import sys
from pathlib import Path

QUEST = Path(__file__).resolve().parents[2]
WS = QUEST / "workspace"
sys.path.insert(0, str(WS))

import main  # noqa

def test_registry_call_and_arg_validation():
    reg = main.ToolRegistry()
    reg.register(main.ToolContract("add", ("a","b"), lambda a,b: a+b))
    assert reg.call("add", a=2, b=3) == 5

    try:
        reg.call("add", a=2)
        assert False, "expected ValueError"
    except ValueError as e:
        assert str(e) == "BAD_ARGS"

    try:
        reg.call("missing", x=1)
        assert False, "expected KeyError"
    except KeyError:
        pass

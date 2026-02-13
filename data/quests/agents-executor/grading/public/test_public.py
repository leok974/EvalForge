import sys
from pathlib import Path

QUEST = Path(__file__).resolve().parents[2]
WS = QUEST / "workspace"
sys.path.insert(0, str(WS))

import main  # noqa

def test_execute_runs_steps():
    # Minimal mock for ToolRegistry
    class ToolContract:
        def __init__(self, name, input_keys, fn):
            self.name = name
            self.input_keys = input_keys
            self.fn = fn

    class ToolRegistry:
        def __init__(self):
            self._tools = {}
        def register(self, tool):
            self._tools[tool.name] = tool
        def call(self, name, **kwargs):
            return self._tools[name].fn(**kwargs)

    reg = ToolRegistry()
    reg.register(ToolContract("add", ("a","b"), lambda a,b: a+b))
    plan = [{"tool":"add","args":{"a":2,"b":3}}, {"tool":"add","args":{"a":3,"b":4}}]
    out = main.execute(plan, reg)
    assert out["results"][0]["output"] == 5
    assert out["results"][1]["output"] == 7


from dataclasses import dataclass
from typing import Callable, Dict

@dataclass(frozen=True)
class ToolContract:
    name: str
    input_keys: tuple[str, ...]
    fn: Callable[..., object]

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, ToolContract] = {}

    def register(self, tool: ToolContract) -> None:
        self._tools[tool.name] = tool

    def call(self, name: str, **kwargs):
        if name not in self._tools:
            raise KeyError(name)
        tool = self._tools[name]
        if set(kwargs.keys()) != set(tool.input_keys):
            raise ValueError("BAD_ARGS")
        return tool.fn(**kwargs)

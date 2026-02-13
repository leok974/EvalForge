
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class ToolContract:
    name: str
    input_keys: tuple[str, ...]
    fn: Callable[..., object]

class ToolRegistry:
    def __init__(self):
        raise NotImplementedError

    def register(self, tool: ToolContract) -> None:
        raise NotImplementedError

    def call(self, name: str, **kwargs):
        raise NotImplementedError

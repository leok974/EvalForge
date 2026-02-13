
class WorkingMemory:
    def __init__(self):
        self._m: dict[str, str] = {}

    def remember(self, key: str, value: str) -> None:
        self._m[key] = value

    def recall(self, key: str, default=None):
        return self._m.get(key, default)

    def forget(self, key: str) -> None:
        self._m.pop(key, None)

    def keys(self, prefix: str = "") -> list[str]:
        out = [k for k in self._m.keys() if k.startswith(prefix)]
        return sorted(out)

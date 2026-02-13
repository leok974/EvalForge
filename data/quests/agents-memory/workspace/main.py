
class WorkingMemory:
    def __init__(self):
        raise NotImplementedError

    def remember(self, key: str, value: str) -> None:
        raise NotImplementedError

    def recall(self, key: str, default=None):
        raise NotImplementedError

    def forget(self, key: str) -> None:
        raise NotImplementedError

    def keys(self, prefix: str = "") -> list[str]:
        raise NotImplementedError

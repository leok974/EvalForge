
class AuditLog:
    def __init__(self):
        raise NotImplementedError

    def event(self, name: str, **fields) -> None:
        raise NotImplementedError

    def span(self, name: str):
        raise NotImplementedError

    def to_json(self) -> list[dict]:
        raise NotImplementedError

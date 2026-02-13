
import contextlib

class AuditLog:
    def __init__(self):
        self._events: list[dict] = []
        self._seq = 0
        self._span_seq = 0

    def event(self, name: str, **fields) -> None:
        self._seq += 1
        e = {"name": name, "seq": self._seq}
        e.update(fields)
        self._events.append(e)

    @contextlib.contextmanager
    def span(self, name: str):
        self._span_seq += 1
        span_id = f"sp{self._span_seq}"
        self.event("span_start", span=name, span_id=span_id)
        try:
            yield span_id
        finally:
            self.event("span_end", span=name, span_id=span_id)

    def to_json(self) -> list[dict]:
        return list(self._events)

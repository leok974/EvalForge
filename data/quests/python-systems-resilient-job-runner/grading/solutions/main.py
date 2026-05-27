from __future__ import annotations
from typing import Callable, TypeVar
import time

T = TypeVar("T")


class RetryError(Exception):
    pass


def run_with_retries(
    job: Callable[[], T],
    *,
    max_attempts: int = 3,
    backoff_seconds: float = 0.1,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> T:
    last_exc: Exception | None = None
    for attempt in range(max_attempts):
        try:
            return job()
        except Exception as exc:
            last_exc = exc
            if attempt < max_attempts - 1:
                sleep_fn(backoff_seconds * (2 ** attempt))
    raise RetryError("all attempts failed") from last_exc

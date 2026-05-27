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
    # TODO: call job() up to max_attempts times
    # TODO: between failures, call sleep_fn(backoff_seconds * (2 ** attempt_index))
    #       where attempt_index starts at 0 for the first failure
    # TODO: if all attempts fail, raise RetryError chaining the last exception
    raise NotImplementedError("TODO: implement run_with_retries")

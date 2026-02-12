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
  if max_attempts <= 0:
    raise ValueError("max_attempts must be >= 1")

  last_exc: BaseException | None = None

  for attempt in range(1, max_attempts + 1):
    try:
      return job()
    except BaseException as e:
      last_exc = e
      if attempt >= max_attempts:
        err = RetryError(f"job failed after {max_attempts} attempts")
        err.__cause__ = last_exc
        raise err
      # backoff on failure #0, #1, ...
      failure_index = attempt - 1
      sleep_fn(backoff_seconds * (2 ** failure_index))

  # unreachable, but makes type-checkers happy
  raise RetryError("unreachable")  # pragma: no cover

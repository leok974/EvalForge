"""
Quest: python-systems-resilient-job-runner

Implement a deterministic retry helper.

Implement:
- class RetryError(Exception)
- run_with_retries(job, *, max_attempts=3, backoff_seconds=0.1, sleep_fn=time.sleep)

Rules:
- call job() until it succeeds
- if job raises, retry until max_attempts is reached
- between failures, call sleep_fn(backoff_seconds * (2 ** (attempt_index)))
  where attempt_index starts at 0 for the first failure.
- if all attempts fail, raise RetryError and chain the last exception as __cause__
"""

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
  raise NotImplementedError("TODO: implement run_with_retries(...)")

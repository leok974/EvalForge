from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class TransientError(Exception):
    pass


class FatalError(Exception):
    pass


def coerce_id(value: Any) -> int:
    try:
        return int(str(value).strip())
    except Exception:
        return 0


def execute_job(job: dict, attempt: int) -> int:
    """
    Execute a single job attempt.

    Kinds:
      - add: always succeeds
      - flaky_add: fails TransientError for first `fail_times` attempts
      - fatal: always fails FatalError
    """
    # TODO: Implement job execution logic
    pass


def run_jobs(jobs: list[dict]) -> list[dict]:
    """
    Pure core runner. Does not print, does not read files.

    Retry policy:
      - max_attempts = 3
      - retry only TransientError
      - FatalError is never retried
    """
    results: list[dict] = []
    max_attempts = 3
    
    # TODO: Implement retry loop
    
    return results

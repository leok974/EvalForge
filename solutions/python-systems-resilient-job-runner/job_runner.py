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
    kind = job.get("kind")
    a = job.get("a")
    b = job.get("b")

    if not isinstance(kind, str) or not isinstance(a, int) or not isinstance(b, int):
        raise FatalError("bad input")

    if kind == "add":
        return a + b

    if kind == "flaky_add":
        fail_times = job.get("fail_times", 0)
        if not isinstance(fail_times, int) or fail_times < 0:
            raise FatalError("bad fail_times")

        if attempt <= fail_times:
            raise TransientError("transient failure")
        return a + b

    if kind == "fatal":
        raise FatalError("fatal failure")

    raise FatalError("unknown kind")


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

    for job in jobs:
        jid = coerce_id(job.get("id"))
        attempts = 0
        ok = False
        value: int | None = None
        error: str | None = None

        for attempt in range(1, max_attempts + 1):
            attempts = attempt
            try:
                value = execute_job(job, attempt)
                ok = True
                error = None
                break
            except TransientError:
                ok = False
                value = None
                error = "EF_RUNNER_RETRY_EXHAUSTED"
                continue
            except FatalError:
                ok = False
                value = None
                error = "EF_RUNNER_FATAL"
                break

        results.append(
            {
                "id": jid,
                "ok": ok,
                "attempts": attempts,
                "value": value,
                "error": error,
            }
        )

    return results

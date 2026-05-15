class TransientError(Exception):
    pass


class FatalError(Exception):
    pass


def execute_job(job: dict, attempt: int) -> int:
    kind = job.get("kind")
    args = job.get("args", [])
    fail_times = job.get("fail_times", 0)

    if kind == "fatal":
        raise FatalError("job is always fatal")
    if kind == "flaky_add" and attempt <= fail_times:
        raise TransientError(f"flaky failure on attempt {attempt}")
    return sum(args)


def run_jobs(jobs: list[dict]) -> list[dict]:
    results = []
    max_attempts = 3
    for job in jobs:
        job_id = job.get("id", 0)
        result = None
        error = None
        attempts = 0
        for attempt in range(1, max_attempts + 1):
            attempts = attempt
            try:
                result = execute_job(job, attempt)
                error = None
                break
            except FatalError:
                error = "EF_RUNNER_FATAL"
                break
            except TransientError:
                if attempt == max_attempts:
                    error = "EF_RUNNER_RETRY_EXHAUSTED"
        results.append({"id": job_id, "ok": error is None, "attempts": attempts,
                         "value": result if error is None else None, "error": error})
    return results

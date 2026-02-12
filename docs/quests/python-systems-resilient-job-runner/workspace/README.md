# Resilient Job Runner

## Objective
Implement a tiny job runner that executes a list of jobs from a fixture file and produces a deterministic run report.

This quest trains resilience fundamentals:
- bounded retries
- retryable vs non-retryable errors
- deterministic behavior (no randomness, stable ordering)
- clean boundaries (core logic does not print or read files)

## Input
A JSON array of jobs in:
- `fixtures/jobs.json`

Each job has:
- `id` (string or number)
- `kind` (string): "add" | "flaky_add" | "fatal"
- `a` (int)
- `b` (int)
- `fail_times` (int, optional): for flaky jobs, how many attempts fail before success

## Behavior
For each job (in fixture order), attempt to execute it.

### Retry Policy
- `max_attempts = 3` (attempts are 1..3)
- Retryable errors: "TransientError" only
- Non-retryable errors: "FatalError" (never retry)

### Job Kinds
- **add**
  - Always succeeds on first attempt.
  - Result is `a + b`.

- **flaky_add**
  - Fails with TransientError for the first `fail_times` attempts.
  - Succeeds afterward (if within max_attempts).
  - Result is `a + b` on success.
  - If it never succeeds within max_attempts, final status is failed with `error="EF_RUNNER_RETRY_EXHAUSTED"`.

- **fatal**
  - Always fails with FatalError on attempt 1.
  - Must not retry.
  - Final status failed with `error="EF_RUNNER_FATAL"`.

### Output
Print exactly one line to stdout: a JSON array of per-job results using canonical formatting:
`json.dumps(out, sort_keys=True, separators=(",",":"))`

The output array must be sorted by `id` ascending.

## Required Result Shape
Each result object must have exactly these keys:
- `id` (int)
- `ok` (bool)
- `attempts` (int)  # number of attempts actually made
- `value` (int|null)
- `error` (string|null)

## Constraints
- Standard library only.
- Core runner must not print or read files.
- Only `main.py` may read the fixture and print stdout.
- Deterministic: no time-based behavior, no randomness.

## Verification
Locally:
```bash
python main.py
```

You should see one JSON line printed.

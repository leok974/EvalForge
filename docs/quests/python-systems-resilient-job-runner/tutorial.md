# Tutorial — Resilient Job Runner

## Approach
You will implement a retry loop with two classes of failures:

- TransientError → retry until max_attempts
- FatalError → fail immediately (no retry)

## Implementation Plan
1. Iterate through jobs.
2. For each job, try attempts 1..3:
   - On success: record ok=true, attempts=current attempt, value=result.
   - On TransientError: continue retrying; if all attempts fail, error=EF_RUNNER_RETRY_EXHAUSTED.
   - On FatalError: stop immediately; error=EF_RUNNER_FATAL.
3. Sort results by id and print canonical JSON once.

## Pitfalls
- Retrying fatal errors (not allowed)
- Off-by-one attempts (must be max 3)
- Printing debug output (breaks stdout JSON)
- Not sorting by id for determinism

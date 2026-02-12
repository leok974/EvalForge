# Hints — Resilient Job Runner

## Hint 1
Use a nested loop: jobs outer loop, attempts inner loop.

## Hint 2
Only retry the transient exception type.

## Hint 3
If attempts 1..3 all fail transiently, final error is EF_RUNNER_RETRY_EXHAUSTED and attempts=3.

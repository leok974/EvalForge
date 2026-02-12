# Hints — Service Boundaries & Contracts

## Hint 1
Core = compute-only. Boundary = IO-only.

## Hint 2
Return a response object every time:
{id, action, ok, value, error}

## Hint 3
For determinism:
- sort by id
- print canonical JSON once

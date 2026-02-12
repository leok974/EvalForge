# Tutorial — Service Boundaries & Contracts

## Approach
Use a two-layer structure:
1) Core logic (`core.py`): compute response from request (no IO).
2) Boundary (`main.py`): load requests, call core, sort, print canonical JSON.

## Implementation Plan
1. Implement `coerce_id` and `handle_request` in `core.py`.
2. For each action:
   - validate inputs
   - return `_ok(...)` on success
   - return `_bad(...)` with correct error code on failure
3. In `main.py`, do NOT add prints besides the final JSON line.

## Pitfalls
- Printing inside core logic (breaks deterministic output)
- Not sorting responses by id
- Returning "" instead of null for error/value
- Using float division; this quest expects integer results from fixture divides

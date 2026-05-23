# Hints: Data Forge

## Hint 1 — Concept
Check the `normalize_record` function. Are you handling the fallback for the "name" field? It should default to "Unknown" if missing or empty.

## Hint 2 — Guided
Use `json.dumps(..., sort_keys=True)` for the final output to match the expected format exactly. Sorting keys ensures a deterministic string output.

## Hint 3 — The Solution
Ensure `id` is an actual `int` before sorting. A common mistake is sorting as strings (`"10"` comes before `"2"`).

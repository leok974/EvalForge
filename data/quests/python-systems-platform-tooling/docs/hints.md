# Hints: Internal Tooling & DX

## Hint 1 — Concept
Use `re.sub(r'[^a-z0-9]+', '-', text.lower())` as a starting point for `slugify`, but remember to clean up duplicate or trailing dashes afterward.

## Hint 2 — Guided
In `unique_sorted`, the `set()` constructor is the most efficient way to deduplicate a list in Python. You can then sort the result.

## Hint 3 — The Solution
Check the `tool` name in `run_tool_request`. The system expects exact string matches (e.g., `"slugify"`, `"unique_sorted"`) and returns an error for unknown tools.

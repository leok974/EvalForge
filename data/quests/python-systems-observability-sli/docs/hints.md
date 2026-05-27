# Hints: Observability & SLI

## Hint 1 — Concept

Iterate over `events` and check each `status_code`. A request is a **success** when `200 <= status_code <= 399`. Accumulate a count:

```python
successes = sum(1 for e in events if 200 <= e["status_code"] <= 399)
```

`399` is a success; `400` is not. This boundary is tested explicitly.

## Hint 2 — Guided

Divide successes by total and round to 4 decimal places:

```python
total = len(events)
return round(successes / total, 4)
```

`round(3 / 13, 4)` → `0.2308`. No need to handle the empty-list case unless the tests require it — check the briefing.

## Hint 3 — The Solution

```python
def calculate_availability(events: list[dict]) -> float:
    total = len(events)
    successes = sum(1 for e in events if 200 <= e["status_code"] <= 399)
    return round(successes / total, 4)
```

Full example with the exact field name the grader uses: `status_code` (not `status`).

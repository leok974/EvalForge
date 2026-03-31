---
id: glossary/python/systems/fail-fast
title: Fail Fast
world: python
level: beginner
tags: [design-principles, error-handling]
related:
  - codex:glossary/python/systems/exception-handling
  - codex:glossary/python/isinstance
---

## Definition
**Fail fast** is a system design principle where execution stops immediately as soon as an unexpected condition or invalid input is detected. Instead of trying to continue with "broken" data, the system raises an error early.

## Why Fail Fast?
- **Easier Debugging**: The error happens exactly where the problem is, not 100 lines later.
- **Data Integrity**: Prevents corrupted data from being saved to a database or sent to another service.
- **Security**: Can prevent certain classes of attacks that rely on malformed inputs.

## Example
```python
def process_positive_number(n):
    # Fail fast: validate input immediately
    if not isinstance(n, (int, float)):
        raise TypeError(f"Expected number, got {type(n)}")
    if n < 0:
        raise ValueError(f"Expected positive number, got {n}")
    
    # Rest of the logic assumes 'n' is valid
    return n * 2
```

## Pitfalls
- Over-using fail-fast in user-facing UIs (where you might want to show all errors at once).
- Not providing clear error messages when failing fast.

## Related
- Exception Handling: Fail fast is implemented by raising exceptions.
- isinstance: Often used for type validation in fail-fast checks.

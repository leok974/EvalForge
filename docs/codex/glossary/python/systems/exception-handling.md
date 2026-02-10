---
id: glossary/python/systems/exception-handling
title: Exception Handling
world: python
level: beginner
tags: [errors, control-flow, debugging]
related:
  - codex:glossary/python/systems/retry
  - codex:glossary/python/systems/timeout
  - codex:glossary/python/keyerror
---

## Definition
**Exception handling** is the process of catching and responding to errors (exceptions) at runtime instead of letting the program crash. Python uses `try/except/finally` blocks to handle exceptions gracefully.

## Usage
- Catch specific exceptions to handle them differently (e.g., `FileNotFoundError`, `ValueError`).
- Use `finally` for cleanup code that must run regardless of errors.
- Avoid bare `except:` — it catches everything, including keyboard interrupts.

## Example
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
    result = None
finally:
    print("Cleanup code runs whether exception occurred or not")

# Better: catch specific exceptions
try:
    data = requests.get(url, timeout=5).json()
except requests.Timeout:
    print("Request timed out")
except requests.HTTPError as e:
    print(f"HTTP error: {e}")
```

## Pitfalls

* Catching `Exception` or bare `except:` hides bugs you didn't anticipate.
* Silently swallowing exceptions (`except: pass`) makes debugging nearly impossible.

## Related

* Retry: retries often wrap exception handling.
* Timeout: timeouts raise exceptions that must be handled.
* KeyError: a specific exception type for missing dictionary keys.
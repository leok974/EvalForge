---
title: Exception Handling in Python
---

# Definition
An **Exception** is an error that occurs during the execution of a program. When Python encounters a situation it cannot handle (like dividing by zero or opening a missing file), it "raises" an exception. If not caught, the program crashes with a "Traceback".

# Why It Matters
Resilient systems must handle "expected" errors gracefully. Instead of crashing, your code can catch the exception, log the error, and either retry or return a friendly message.

# The `try-except` Block
```python
try:
    # Code that might fail
    with open("config.json") as f:
        data = f.read()
except FileNotFoundError:
    # Recovery logic
    print("Warning: config.json missing. Using defaults.")
    data = "{}"
except Exception as e:
    # Catch-all for unexpected errors (use sparingly)
    print(f"An unexpected error occurred: {e}")
finally:
    # Always runs, regardless of success or failure
    print("Cleanup complete.")
```

# Common Mistakes
- **Silent Failure**: Catching an exception but doing nothing (`pass`). This makes debugging nearly impossible.
- **Generic Catch**: Catching `Exception` at the top level without specific handlers below it. Always catch specific errors (e.g., `ValueError`, `KeyError`) first.

# In EvalForge
We use exceptions to signal "Data Contract" violations in our System Engineering tracks.

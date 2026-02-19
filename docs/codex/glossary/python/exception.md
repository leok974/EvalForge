---
title: Exception
---

# Definition
An error detected during execution.

# Why It Matters
Allows programs to handle errors gracefully instead of crashing.

# Minimal Example
```python
try:\n    x = 1/0\nexcept ZeroDivisionError:\n    print('Oops')
```

# Common Mistakes
* Catching generic `Exception` without logging.

# In EvalForge
* Key for writing robust logic.

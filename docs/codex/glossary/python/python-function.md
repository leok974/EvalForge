---
title: Python Functions
---

# Definition
A **Function** is a named, reusable block of code that performs a specific action. Functions can take inputs (**arguments**) and produce an output (**return value**).

# Why It Matters
- **DRY (Don't Repeat Yourself)**: Write logic once, use it everywhere.
- **Abstraction**: Hide complex logic behind a simple name (e.g., `calculate_tax()`).
- **Testability**: Pure functions (no side effects) are easy to verify.

# Anatomy of a Function
```python
def greet(name: str, shout: bool = False) -> str:
    """A docstring explaining what the function does."""
    message = f"Hello, {name}!"
    if shout:
        return message.upper()
    return message

# Usage
msg = greet("Alice", shout=True)
print(msg) # Output: HELLO, ALICE!
```

# Scope
Variables defined inside a function are **local** to that function. They cannot be accessed from the outside.

# Common Mistakes
- **Missing `return`**: If you forget `return`, the function returns `None` by default.
- **Mutable Defaults**: Never use a list or dict as a default argument (e.g., `def add(item, my_list=[])`). Use `None` instead.

# In EvalForge
Functions are the primary unit of grading in most Python quests.

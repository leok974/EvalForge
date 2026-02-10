---
id: glossary/python/keyerror
title: KeyError
world: python
level: beginner
tags: [errors, dictionaries, debugging]
related:
  - codex:glossary/python/dictionary
  - codex:glossary/python/systems/exception-handling
  - codex:glossary/python/systems/module-not-found-error
---

## Definition
**KeyError** is raised when you try to access a dictionary key that doesn't exist. This is one of the most common Python errors and indicates missing data or a typo in the key name.

## Usage
- Use `.get(key, default)` instead of `dict[key]` to avoid KeyError.
- Catch KeyError with try/except when the key might be missing.
- Check if a key exists with `key in dict` before accessing.

## Example
```python
user = {"name": "Alice"}

# This raises KeyError
try:
    print(user["age"])
except KeyError:
    print("Age not found")

# Better: use .get() with default
age = user.get("age", "Unknown")
print(age)  # "Unknown"

# Check if key exists
if "email" in user:
    print(user["email"])
```

## Pitfalls

* Typos in key names cause KeyError; use constants or enums for common keys.
* Silently catching KeyError without logging hides data issues.

## Related

* Dictionary: KeyError occurs with dictionary access.
* Exception Handling: catch KeyError to handle missing keys gracefully.
* ModuleNotFoundError: similar error for missing Python modules.
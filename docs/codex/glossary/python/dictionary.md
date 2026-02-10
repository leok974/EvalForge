---
id: glossary/python/dictionary
title: Dictionary
world: python
level: beginner
tags: [data-structures, basics, collections]
related:
  - codex:glossary/python/keyerror
  - codex:glossary/python/iteration
  - codex:glossary/python/for-loop
---

## Definition
A **dictionary** (dict) is a mutable, unordered collection of key-value pairs. Dictionaries provide O(1) average-case lookup, making them ideal for fast data retrieval by key.

## Usage
- Store mappings between keys and values.
- Use `dict.get(key, default)` to avoid KeyError.
- Iterate over keys, values, or key-value pairs.

## Example
```python
# Create a dictionary
user = {"name": "Alice", "age": 30, "email": "alice@example.com"}

# Access values
print(user["name"])  # "Alice"

# Safe access with default
print(user.get("phone", "N/A"))  # "N/A"

# Iterate over dictionary
for key, value in user.items():
    print(f"{key}: {value}")

# Add/update keys
user["phone"] = "555-1234"
```

## Pitfalls

* Accessing missing keys with `dict[key]` raises KeyError; use `.get()` for safety.
* Dictionaries are unordered (before Python 3.7); don't rely on insertion order in old code.

## Related

* KeyError: raised when accessing missing dict keys.
* Iteration: iterate over dict keys, values, or items.
* For Loop: commonly used to loop over dictionaries.
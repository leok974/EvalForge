---
id: glossary/python/isinstance
title: isinstance
world: python
level: beginner
tags: [built-ins, typing, validation]
related:
  - codex:glossary/python/typing
  - codex:glossary/python/python-function
---

## Definition
`isinstance(object, classinfo)` is a built-in Python function that returns `True` if the `object` is an instance of the `classinfo` (or a subclass thereof), and `False` otherwise.

## Usage
- Use it to validate that inputs match the expected type.
- Prefer `isinstance()` over `type(x) == Y` because it supports inheritance.
- Pass a tuple of types to check against multiple options: `isinstance(x, (int, float))`.

## Example
```python
def add_one(x):
    if not isinstance(x, int):
        raise TypeError("x must be an integer")
    return x + 1

print(isinstance(5, int))    # True
print(isinstance("5", int))  # False
```

## Pitfalls
- Over-use of `isinstance` can sometimes be a sign that you should use duck typing or interfaces instead.
- Checking for `list` or `dict` specifically might be too restrictive if any sequence or mapping would work.

## Related
- Typing: Often used in conjunction with type hints for runtime validation.
- Python Function: Frequently used inside function bodies for safety.

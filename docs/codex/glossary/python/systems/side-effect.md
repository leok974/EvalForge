---
id: glossary/python/systems/side-effect
title: Side Effect
world: python
level: intermediate
tags: [functions, architecture, debugging]
related:
  - codex:glossary/python/systems/idempotency
  - codex:glossary/python/systems/exception-handling
  - codex:glossary/python/dictionary
---

## Definition
A **side effect** is any observable change a function makes beyond returning a value: modifying a global variable, writing to a file, sending a network request, or mutating input arguments. Pure functions have no side effects.

## Usage
- Minimize side effects to make code predictable and testable.
- Document side effects in docstrings.
- Isolate side effects in specific functions (e.g., `save_to_db()`, `send_email()`)

## Example
```python
# No side effects (pure function)
def add(a, b):
    return a + b

# Side effect: modifies global state
counter = 0
def increment_counter():
    global counter
    counter += 1  # Side effect

# Side effect: mutates input
def append_item(items, item):
    items.append(item)  # Mutates input list

# Better: return new list (no side effect)
def append_item_pure(items, item):
    return items + [item]
```

## Pitfalls

* Hidden side effects make debugging hard — functions appear to work but change global state.
* Mutating input arguments surprises callers who expect immutability.

## Related

* Idempotency: side effects complicate idempotent operations.
* Exception Handling: side effects can leave partial state if exceptions occur.
* Dictionary: mutating dict arguments is a common hidden side effect.
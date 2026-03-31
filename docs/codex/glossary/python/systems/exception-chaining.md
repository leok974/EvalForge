---
id: glossary/python/systems/exception-chaining
title: Exception Chaining
world: python
level: intermediate
tags: [errors, debugging, resilience]
related:
  - codex:glossary/python/systems/exception-handling
  - codex:glossary/python/exception
---

## Definition
**Exception chaining** is a technique in Python used to preserve the context of an original error when raising a new, more high-level exception. By using the `raise NewException from e` syntax, you create a "cause" link that shows both errors in the traceback.

## Usage
- Use chaining when you want to catch a low-level error (like `IOError`) and re-raise it as a domain-specific error (like `ConfigurationError`).
- It helps maintain a clear "paper trail" for debugging.

## Example
```python
try:
    with open("config.json") as f:
        config = json.load(f)
except FileNotFoundError as e:
    # Preserve 'e' as the cause of the new error
    raise ConfigurationError("Application failed to load config") from e
```

## Traceback Appearance
The traceback will explicitly state: 
`The above exception was the direct cause of the following exception:`

## Pitfalls
- Raising a new exception *without* `from e` (unless intentional) can make it harder to find the root cause, though Python 3 still shows the "during handling of..." context.
- `raise ... from None` can be used to explicitly *hide* the original cause if it's considered sensitive or distracting.

## Related
- Exception Handling: Chaining is a subset of handling.
- Exception: The base concept for all errors.

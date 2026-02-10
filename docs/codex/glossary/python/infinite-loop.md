---
id: glossary/python/infinite-loop
title: Infinite Loop
world: python
level: beginner
tags: [control-flow, debugging, loops]
related:
  - codex:glossary/python/for-loop
  - codex:glossary/python/break-continue
  - codex:glossary/python/systems/timeout
---

## Definition
An **infinite loop** is a loop that never terminates because its exit condition is never met. While some infinite loops are intentional (event loops, servers), most are bugs that cause programs to hang.

## Usage
- Use `while True:` for intentional infinite loops (servers, event processors).
- Always include a `break` condition to exit intentional infinite loops.
- Avoid infinite loops caused by logic errors in loop conditions.

## Example
```python
# Intentional infinite loop (server)
while True:
    request = get_next_request()
    process_request(request)
    if should_shutdown():
        break  # Exit condition

# Accidental infinite loop (bug)
i = 0
while i < 10:
    print(i)
    # BUG: forgot to increment i, loops forever!

# Fixed
i = 0
while i < 10:
    print(i)
    i += 1  # Now loop terminates
```

## Pitfalls

* Forgetting to update loop variables causes infinite loops.
* Using `while True:` without a `break` makes loops impossible to exit.

## Related

* For Loop: for loops have built-in termination; while loops can be infinite.
* Break/Continue: break is essential for exiting infinite loops.
* Timeout: use timeouts to detect and kill infinite loops.
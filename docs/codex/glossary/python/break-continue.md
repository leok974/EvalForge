---
id: glossary/python/break-continue
title: Break & Continue
world: python
level: beginner
tags: [control-flow, loops, basics]
related:
  - codex:glossary/python/for-loop
  - codex:glossary/python/infinite-loop
  - codex:glossary/python/iteration
---

## Definition
**Break** exits a loop immediately, while **continue** skips the rest of the current iteration and moves to the next one. These keywords give you fine-grained control over loop execution.

## Usage
- Use `break` to exit a loop early when a condition is met.
- Use `continue` to skip processing for specific items.
- Avoid overusing; sometimes restructuring the loop is clearer.

## Example
```python
# break: exit loop early
for i in range(10):
    if i == 5:
        break  # Stop loop when i reaches 5
    print(i)  # Prints 0, 1, 2, 3, 4

# continue: skip to next iteration
for i in range(5):
    if i == 2:
        continue  # Skip when i == 2
    print(i)  # Prints 0, 1, 3, 4

# Search with break
numbers = [1, 3, 7, 9, 11]
for num in numbers:
    if num > 5:
        print(f"Found first number > 5: {num}")
        break
```

## Pitfalls

* Using `break` in nested loops only exits the inner loop, not the outer one.
* Overusing `continue` makes control flow hard to follow; consider filtering beforehand.

## Related

* For Loop: break and continue control loop execution.
* Infinite Loop: break is essential for exiting infinite loops.
* Iteration: break and continue affect iteration flow.
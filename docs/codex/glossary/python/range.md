---
id: glossary/python/range
title: Range
world: python
level: beginner
tags: [built-ins, loops, basics]
related:
  - codex:glossary/python/for-loop
  - codex:glossary/python/iteration
  - codex:glossary/python/systems/time-complexity
---

## Definition
**Range** is a built-in function that generates a sequence of numbers. It's commonly used in for loops to iterate a specific number of times. `range()` is memory-efficient because it generates numbers on demand, not all at once.

## Usage
- `range(n)` generates 0 to n-1.
- `range(start, stop)` generates start to stop-1.
- `range(start, stop, step)` generates numbers with custom step.

## Example
```python
# range(5) generates 0, 1, 2, 3, 4
for i in range(5):
    print(i)

# range(2, 6) generates 2, 3, 4, 5
for i in range(2, 6):
    print(i)

# range with step
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# Reverse range
for i in range(5, 0, -1):
    print(i)  # 5, 4, 3, 2, 1
```

## Pitfalls

* `range(n)` starts at 0, not 1 — forgetting this causes off-by-one errors.
* Converting `range()` to a list with `list(range(1000000))` wastes memory; iterate directly.

## Related

* For Loop: range is commonly used in for loops.
* Iteration: range generates sequences for iteration.
* Time Complexity: understanding range helps analyze loop complexity.
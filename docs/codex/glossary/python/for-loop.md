---
id: glossary/python/for-loop
title: For Loop
world: python
level: beginner
tags: [control-flow, iteration, basics]
related:
  - codex:glossary/python/iteration
  - codex:glossary/python/range
  - codex:glossary/python/break-continue
---

## Definition
A **for loop** iterates over a sequence (list, string, range) and executes a block of code for each element. For loops are the primary way to process collections in Python.

## Usage
- Loop over lists, strings, dicts, or any iterable.
- Use `range()` for numeric sequences.
- Access both index and value with `enumerate()`.

## Example
```python
# Loop over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Loop with range
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# Loop with index and value
for idx, fruit in enumerate(fruits):
    print(f"{idx}: {fruit}")
```

## Pitfalls

* Modifying a list while looping over it causes unexpected behavior; iterate over a copy instead.
* Nested for loops can become O(n²) — watch performance with large datasets.

## Related

* Iteration: for loops perform iteration.
* Range: creates numeric sequences for loops.
* Break/Continue: control loop execution.
---
id: glossary/python/iteration
title: Iteration
world: python
level: beginner
tags: [control-flow, loops, basics]
related:
  - codex:glossary/python/for-loop
  - codex:glossary/python/range
  - codex:glossary/python/dictionary
---

## Definition
**Iteration** is the process of repeatedly executing code for each item in a sequence or iterable. Python's for loops, comprehensions, and iterators all perform iteration.

## Usage
- Iterate over lists, strings, dicts, sets, or any iterable object.
- Use iterators (`iter()`) and generators for memory-efficient iteration.
- Combine iteration with filtering, mapping, or aggregation.

## Example
```python
# Iterate over a list
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    print(num)

# List comprehension (iteration + transformation)
squares = [x**2 for x in numbers]

# Iterate over a dict
user = {"name": "Alice", "age": 30}
for key in user:
    print(f"{key}: {user[key]}")

# Custom iterator
class Counter:
    def __init__(self, max):
        self.max = max
        self.n = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.n < self.max:
            result = self.n
            self.n += 1
            return result
        raise StopIteration
```

## Pitfalls

* Creating large lists for iteration wastes memory; use generators instead.
* Infinite iteration (no termination condition) causes hangs.

## Related

* For Loop: the primary iteration construct.
* Range: generates numeric sequences for iteration.
* Dictionary: iterating over dict keys, values, or items.
---
id: glossary/python/systems/bottleneck
title: Bottleneck
world: python
level: intermediate
tags: [performance, profiling, optimization]
related:
  - codex:glossary/python/systems/profiling
  - codex:glossary/python/systems/hot-path
  - codex:glossary/python/systems/time-complexity
---

## Definition
A **bottleneck** is the slowest part of a system that limits overall performance. Identifying bottlenecks (via profiling) lets you focus optimization efforts where they'll have the biggest impact.

## Usage
- Profile your code to find bottlenecks (CPU, I/O, memory, network).
- Optimize the bottleneck first before making other changes.
- After fixing one bottleneck, re-profile — a new bottleneck often appears.

## Example
```python
import cProfile

def slow_function():
    total = 0
    for i in range(1_000_000):  # This loop is the bottleneck
        total += i ** 2
    return total

# Profile to find the bottleneck
cProfile.run('slow_function()')
# Output shows slow_function took 99% of execution time
```

## Pitfalls

* Optimizing non-bottleneck code wastes time and adds complexity.
* Assuming the bottleneck without profiling often leads you to optimize the wrong thing.

## Related

* Profiling: profiling identifies bottlenecks.
* Hot Path: the hot path often contains the bottleneck.
* Time Complexity: bottlenecks often have high time complexity.
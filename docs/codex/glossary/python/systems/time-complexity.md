---
id: glossary/python/systems/time-complexity
title: Time Complexity
world: python
level: intermediate
tags: [algorithms, performance, big-o]
related:
  - codex:glossary/python/systems/bottleneck
  - codex:glossary/python/systems/profiling
  - codex:glossary/python/for-loop
---

## Definition
**Time complexity** describes how an algorithm's runtime grows as input size increases, expressed in Big-O notation (O(n), O(log n), etc.). Understanding time complexity helps you pick algorithms that scale and avoid performance problems.

## Usage
- Prefer O(1) constant time operations when possible.
- Avoid O(n²) nested loops on large datasets.
- Use appropriate data structures: dict lookups are O(1), list searches are O(n).

## Example
```python
# O(1) - constant time
def get_first(items):
    return items[0]

# O(n) - linear time
def find_max(items):
    return max(items)

# O(n²) - quadratic time (inefficient)
def find_duplicates_slow(items):
    duplicates = []
    for i in items:
        for j in items:
            if i == j and i not in duplicates:
                duplicates.append(i)
    return duplicates

# O(n) - better approach
def find_duplicates_fast(items):
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)
```

## Pitfalls

* Ignoring time complexity leads to code that works fine in development but fails in production with large datasets.
* Nested loops (`for x in items: for y in items:`) are often O(n²) — avoid when n is large.

## Related

* Bottleneck: high time complexity code paths become bottlenecks.
* Profiling: profiling reveals where time complexity matters most.
* For Loop: understanding loop complexity is critical.
---
id: glossary/python/systems/cprofile
title: cProfile
world: python
level: intermediate
tags: [profiling, performance, tooling]
related:
  - codex:glossary/python/systems/profiling
  - codex:glossary/python/systems/bottleneck
  - codex:glossary/python/systems/hot-path
---

## Definition
**cProfile** is Python's built-in profiler that measures how much time is spent in each function. It's the go-to tool for finding performance bottlenecks in CPU-bound code.

## Usage
- Run `python -m cProfile script.py` to profile entire scripts.
- Use `cProfile.Profile()` to profile specific code sections.
- Analyze results with `pstats` to sort by time, calls, or cumulative duration.

## Example
```python
import cProfile

def slow_loop():
    total = 0
    for i in range(1_000_000):
        total += i ** 2
    return total

# Profile a function
cProfile.run('slow_loop()')

# Command-line profiling
# python -m cProfile -s cumtime script.py
```

## Pitfalls

* cProfile adds overhead; results show relative time, not absolute wall-clock time.
* Too much noise from library calls; filter results to focus on your code.

## Related

* Profiling: cProfile is a profiling tool.
* Bottleneck: use cProfile to find bottlenecks.
* Hot Path: profile the hot path to optimize effectively.
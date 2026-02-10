---
id: glossary/python/systems/profiling
title: Profiling
world: python
level: intermediate
tags: [performance, debugging, optimization]
related:
  - codex:glossary/python/systems/cprofile
  - codex:glossary/python/systems/bottleneck
  - codex:glossary/python/systems/hot-path
---

## Definition
**Profiling** measures where your program spends time and resources (CPU, memory). Use profiling to identify bottlenecks before optimizing — guessing at performance problems is usually wrong.

## Usage
- Profile before optimizing to find the actual slow parts.
- Use `cProfile` for CPU profiling or `memory_profiler` for memory usage.
- Focus optimization on the top 3-5 functions consuming the most time.

## Example
```python
import cProfile
import pstats

def compute():
    return sum(i**2 for i in range(1_000_000))

# Profile the function
profiler = cProfile.Profile()
profiler.enable()
compute()
profiler.disable()

# Print stats sorted by cumulative time
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

## Pitfalls

* Profiling in development doesn't always match production performance (different data, load, hardware).
* Over-optimizing based on micro-benchmarks instead of real-world usage.

## Related

* cProfile: Python's built-in profiler.
* Bottleneck: profiling reveals bottlenecks.
* Hot Path: profile the hot path to find the biggest wins.
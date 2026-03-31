# Performance Profiling

**Performance Profiling** is the process of measuring the resource usage (time, memory, CPU) of a program to identify bottlenecks.

## Core Concepts
- **Bottleneck**: The slowest part of a system that limits overall throughput.
- **Big O Notation**: A mathematical way to describe how the execution time or space requirements grow as the input size increases.
- **Hot Path**: The segment of code that is executed most frequently and where optimizations have the highest impact.

## Benchmarking vs. Profiling
- **Benchmarking**: Measuring how long the *entire* task takes.
- **Profiling**: Measuring how long *each part* of the task takes.

## Deterministic Profiling
In many educational environments, we use "Op Counting" (counting comparisons or lookups) to provide deterministic profiling results that don't depend on system clock resolution.

## Related
- [Time Complexity](codex:glossary/python/systems/time-complexity)
- [Bottleneck](codex:glossary/python/systems/bottleneck)
- [cProfile](codex:glossary/python/systems/cprofile)

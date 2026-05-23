---
title: Performance Basics
id: glossary/java/memory/performance-basics
world: java
level: intermediate
tags: [java, optimization, metrics]
related:
  - codex:glossary/java/fundamentals/jvm
  - codex:glossary/java/memory/garbage-collection
  - codex:glossary/java/concurrency/threads
---

# Performance Basics

## Definition
Performance basics in Java revolve around CPU vs memory tradeoffs, allocation pressure, and JVM warmup. JIT compilation and GC behavior can make performance non-intuitive.

## Usage
- Measure before optimizing.
- Look for allocation hotspots.
- Avoid blocking operations on critical threads.

## Example
```java
long t0 = System.nanoTime();
// work
long ms = (System.nanoTime() - t0) / 1_000_000;
System.out.println("ms=" + ms);
```

## Pitfalls

* Microbenchmarks are misleading without proper methodology (warmup, isolation).
* "Faster" code that increases allocations can regress overall performance.

## Related

* JVM: JVM optimizations affect performance.
* Garbage Collection: GC pauses affect performance.
* Threads: concurrency affects throughput.

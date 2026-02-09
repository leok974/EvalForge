---
title: Garbage Collection
id: glossary/java/memory/garbage-collection
world: java
level: intermediate
tags: [java, memory, internals]
related:
  - codex:glossary/java/fundamentals/jvm
  - codex:glossary/java/memory/performance-basics
---

# Garbage Collection

## Definition
**Garbage collection (GC)** automatically reclaims memory from objects no longer referenced. The JVM uses different GC strategies to balance throughput and pause times.

## Usage
- Monitor memory usage and GC pauses.
- Tune heap sizes (`-Xms`, `-Xmx`).
- Reduce allocations in hot paths.

## Example
```bash
java -Xms512m -Xmx512m -jar app.jar
# Monitor: jcmd / jstat / profiler tooling (conceptually)
```

## Pitfalls

* High allocation rates can cause frequent GC pauses even with "enough" memory.
* Holding references (caches, static maps) can prevent collection and look like leaks.

## Related

* JVM: JVM runs the GC.
* Performance Basics: GC impacts performance.

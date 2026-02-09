---
title: Executors
id: glossary/java/concurrency/executors
world: java
level: intermediate
tags: [java, concurrency, threading]
related:
  - codex:glossary/java/concurrency/threads
  - codex:glossary/java/concurrency/synchronization
---

# Executors

## Definition
**Executors** manage thread pools and task scheduling. Instead of creating raw threads, you submit tasks to an executor for controlled concurrency.

## Usage
- Use fixed thread pools for bounded concurrency.
- Use scheduled executors for recurring tasks.
- Shut down executors gracefully.

## Example
```java
ExecutorService pool = Executors.newFixedThreadPool(4);
Future<Integer> f = pool.submit(() -> 42);
int result = f.get();
pool.shutdown();
```

## Pitfalls

* Forgetting to shut down pools can keep the JVM running.
* Unbounded queues can cause memory growth under load.

## Related

* Threads: executors abstract thread management.
* Synchronization: tasks often need synchronization.

---
title: Threads
id: glossary/java/concurrency/threads
world: java
level: intermediate
tags: [java, concurrency, multitasking]
related:
  - codex:glossary/java/concurrency/executors
  - codex:glossary/java/concurrency/synchronization
  - codex:glossary/java/language/immutability
---

# Threads

## Definition
A **thread** is an independent path of execution within a process. Threads share memory, so concurrency bugs often come from shared mutable state.

## Usage
- Run work in parallel for responsiveness or throughput.
- Use thread-safe data and clear ownership.
- Prefer higher-level executors over manual thread management.

## Example
```java
Thread t = new Thread(() -> System.out.println("work"));
t.start();
t.join();
```

## Pitfalls

* Data races occur when multiple threads write/read shared data unsafely.
* Creating too many threads can reduce performance (context switching).

## Related

* Executors: executors manage threads efficiently.
* Synchronization: synchronization protects shared state.
* Immutability: immutable objects are thread-safe.

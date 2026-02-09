---
title: Synchronization
id: glossary/java/concurrency/synchronization
world: java
level: intermediate
tags: [java, concurrency, safety]
related:
  - codex:glossary/java/concurrency/threads
  - codex:glossary/java/concurrency/executors
  - codex:glossary/java/language/immutability
---

# Synchronization

## Definition
**Synchronization** coordinates access to shared state across threads to avoid races. Common tools: `synchronized`, `Lock`, `volatile`, and concurrent collections.

## Usage
- Protect critical sections that mutate shared data.
- Use `volatile` for visibility (not atomicity).
- Prefer immutability and message passing when possible.

## Example
```java
class Counter {
  private int value = 0;
  synchronized void inc() { value++; }
  synchronized int get() { return value; }
}
```

## Pitfalls

* Deadlocks happen when locks are acquired in inconsistent order.
* Over-synchronization can kill performance.

## Related

* Threads: threads need synchronization for shared state.
* Executors: concurrent tasks need synchronization.
* Immutability: reduce the need for synchronization.

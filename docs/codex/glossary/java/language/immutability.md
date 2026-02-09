---
title: Immutability
id: glossary/java/language/immutability
world: java
level: intermediate
tags: [java, design, concurrency]
related:
  - codex:glossary/java/concurrency/synchronization
  - codex:glossary/java/concurrency/threads
  - codex:glossary/java/collections/collections-framework
---

# Immutability

## Definition
**Immutability** means an object's state cannot change after construction. Immutable data is easier to reason about and much safer in concurrent programs.

## Usage
- Prefer `final` fields.
- Use immutable collections where possible.
- Model data as values, not mutable bags.

## Example
```java
public record User(String id, String email) {}
```

## Pitfalls

* "Immutable" objects that contain mutable fields (like a modifiable list) aren't truly immutable.
* Excess copying can be expensive—balance safety and performance.

## Related

* Synchronization: immutable objects often don't need synchronization.
* Threads: immutability simplifies thread safety.
* Collections Framework: use immutable collections.

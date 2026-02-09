---
title: Collections Framework
id: glossary/java/collections/collections-framework
world: java
level: beginner
tags: [java, data-structures, api]
related:
  - codex:glossary/java/language/generics
  - codex:glossary/java/language/immutability
  - codex:glossary/java/concurrency/synchronization
---

# Collections Framework

## Definition
The **Collections Framework** is Java's standard set of data structures: `List`, `Set`, `Map`, plus implementations like `ArrayList`, `HashSet`, `HashMap`. Choosing the right structure impacts performance and correctness.

## Usage
- `List` for ordered items.
- `Set` for uniqueness.
- `Map` for key/value lookup.
- Prefer interfaces in types (`List`, not `ArrayList`).

## Example
```java
Map<String, Integer> counts = new HashMap<>();
counts.put("ok", 1);
counts.merge("ok", 1, Integer::sum); // now 2
```

## Pitfalls

* `HashMap` has no guaranteed iteration order (use `LinkedHashMap` if needed).
* Mutating collections shared across threads requires synchronization or concurrent collections.

## Related

* Generics: collections use generics for type safety.
* Immutability: immutable collections are safer.
* Synchronization: shared mutable collections need synchronization.

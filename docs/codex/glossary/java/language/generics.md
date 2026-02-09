---
title: Generics
id: glossary/java/language/generics
world: java
level: intermediate
tags: [java, type-safety, collections]
related:
  - codex:glossary/java/collections/collections-framework
  - codex:glossary/java/language/immutability
---

# Generics

## Definition
**Generics** provide compile-time type safety for collections and APIs (e.g., `List<String>`). They reduce casting and make code safer and clearer.

## Usage
- Use parameterized types in collections.
- Define generic methods/classes for reusable logic.
- Avoid raw types.

## Example
```java
List<String> names = List.of("Ada", "Linus");
// names.add(123); // compile error
```

## Pitfalls

* Type erasure means generic type info is mostly gone at runtime.
* Raw types (`List list`) reintroduce unsafe casts and warnings.

## Related

* Collections Framework: generics are essential for collections.
* Immutability: generics help define immutable types.

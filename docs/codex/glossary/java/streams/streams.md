---
title: Streams
id: glossary/java/streams/streams
world: java
level: intermediate
tags: [java, functional, collections]
related:
  - codex:glossary/java/collections/collections-framework
  - codex:glossary/java/memory/performance-basics
---

# Streams

## Definition
Java **Streams** provide a functional pipeline for processing collections: map/filter/reduce with lazy evaluation. They improve readability for transformations and aggregations.

## Usage
- Transform and filter collections.
- Aggregate values (`count`, `sum`, `collect`).
- Avoid manual loops for simple pipelines.

## Example
```java
List<String> out =
  names.stream()
       .filter(n -> n.length() > 3)
       .map(String::toUpperCase)
       .toList();
```

## Pitfalls

* Streams are not automatically "faster" than loops; they trade performance for expressiveness.
* Side effects inside stream operations can cause bugs (especially parallel streams).

## Related

* Collections Framework: streams process collections.
* Performance Basics: understand stream performance tradeoffs.

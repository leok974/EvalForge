---
title: Exceptions
id: glossary/java/language/exceptions
world: java
level: beginner
tags: [java, error-handling, control-flow]
related:
  - codex:glossary/java/language/immutability
  - codex:glossary/java/testing/junit-basics
---

# Exceptions

## Definition
An **exception** is an error signal that interrupts normal control flow. Java distinguishes **checked exceptions** (must be handled/declared) from **unchecked exceptions** (RuntimeException subclasses).

## Usage
- Use exceptions for exceptional conditions, not ordinary branching.
- Wrap low-level exceptions with context.
- Prefer specific exceptions over catch-all.

## Example
```java
try {
  Files.readString(Path.of("config.json"));
} catch (IOException e) {
  throw new IllegalStateException("Failed to load config", e);
}
```

## Pitfalls

* Catching `Exception` hides bugs and makes debugging harder.
* Swallowing exceptions ("catch and ignore") causes silent corruption.

## Related

* Immutability: immutable objects simplify exception safety.
* JUnit Basics: tests should verify exception handling.

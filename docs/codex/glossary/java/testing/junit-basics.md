---
title: JUnit Basics
id: glossary/java/testing/junit-basics
world: java
level: beginner
tags: [java, testing, tdd]
related:
  - codex:glossary/java/language/exceptions
  - codex:glossary/java/build/maven-vs-gradle
---

# JUnit Basics

## Definition
**JUnit** is a test framework for Java. Tests assert expected behavior and protect against regressions during refactors.

## Usage
- Write small tests per behavior.
- Use assertions to document intent.
- Run tests in CI via Maven/Gradle.

## Example
```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class MathTest {
  @Test void adds() {
    assertEquals(4, 2 + 2);
  }
}
```

## Pitfalls

* Tests that depend on ordering or time are flaky.
* Over-mocking can make tests meaningless; prefer real behavior tests.

## Related

* Exceptions: tests verify exception behavior.
* Maven vs Gradle: build tools run JUnit tests.

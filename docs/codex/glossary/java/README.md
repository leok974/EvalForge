---
title: Java Glossary
id: glossary/java/README
world: java
level: beginner
tags: [java, glossary, fundamentals]
---

# Java Glossary

## Definition
Java is a general-purpose, strongly-typed language built around the JVM. In EvalForge, the Java world focuses on runtime fundamentals (JVM, classpath, bytecode), safe concurrency, modern collections/streams, and test-driven development with JUnit.

## How to use this Codex
- Use **JVM / Bytecode / Classpath** when you're debugging runtime issues.
- Use **Threads / Executors / Synchronization** when you're building concurrent systems.
- Use **Exceptions / Immutability / Garbage Collection** when you're writing reliable code.
- Use **Maven vs Gradle / JUnit Basics** for build + testing workflows.

## Example
```bash
# Conceptual workflow
mvn test
# or
./gradlew test
```

## Pitfalls

* Many Java errors are "runtime environment" issues (classpath, versions), not code bugs.
* Concurrency issues can be intermittent—prefer safe defaults (executors, immutability).

## Related

* [[glossary/java/fundamentals/jvm]]
* [[glossary/java/fundamentals/classpath]]
* [[glossary/java/fundamentals/bytecode]]
* [[glossary/java/build/maven-vs-gradle]]
* [[glossary/java/testing/junit-basics]]

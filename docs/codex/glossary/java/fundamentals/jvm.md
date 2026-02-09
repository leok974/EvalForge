---
title: JVM
id: glossary/java/fundamentals/jvm
world: java
level: beginner
tags: [java, runtime, internals]
related:
  - codex:glossary/java/fundamentals/bytecode
  - codex:glossary/java/fundamentals/classpath
  - codex:glossary/java/memory/garbage-collection
---

# JVM

## Definition
The **JVM (Java Virtual Machine)** executes Java bytecode. It manages memory (heap/stack), runs the garbage collector, and uses JIT compilation to optimize hot code paths while the program runs.

## Usage
- Understand performance behavior (warmup, JIT, GC pauses).
- Debug runtime issues (class loading, memory errors).
- Choose runtime flags and observe metrics.

## Example
```bash
java -version
java -Xms256m -Xmx512m -jar app.jar
```

## Pitfalls

* Performance can change after warmup due to JIT compilation.
* Memory issues may be GC tuning problems, not leaks in the classic sense.

## Related

* Bytecode: JVM executes bytecode.
* Classpath: JVM loads classes from the classpath.
* Garbage Collection: JVM manages memory via GC.

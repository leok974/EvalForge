---
title: Bytecode
id: glossary/java/fundamentals/bytecode
world: java
level: intermediate
tags: [java, compilation, internals]
related:
  - codex:glossary/java/fundamentals/jvm
  - codex:glossary/java/fundamentals/classpath
---

# Bytecode

## Definition
**Bytecode** is the intermediate instruction format produced by the Java compiler (`javac`). The JVM executes bytecode, allowing Java programs to run on many platforms.

## Usage
- Explains "compile once, run anywhere".
- Helps when debugging class version and compatibility errors.
- Relevant for tooling (profilers, debuggers).

## Example
```bash
javac Hello.java
javap -c Hello.class
```

## Pitfalls

* "Unsupported major.minor version" means you compiled for a newer JVM than you're running.
* Reflection and dynamic proxies still run bytecode—but can be harder to reason about.

## Related

* JVM: JVM executes bytecode.
* Classpath: JVM finds bytecode on the classpath.

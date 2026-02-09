---
title: Classpath
id: glossary/java/fundamentals/classpath
world: java
level: beginner
tags: [java, configuration, dependencies]
related:
  - codex:glossary/java/fundamentals/jvm
  - codex:glossary/java/language/exceptions
  - codex:glossary/java/build/maven-vs-gradle
---

# Classpath

## Definition
The **classpath** is the set of locations (directories/jars) the JVM searches to load classes. If a class isn't on the classpath, you get `ClassNotFoundException` or `NoClassDefFoundError`.

## Usage
- Run apps with external libs.
- Control which versions of dependencies are loaded.
- Debug "it compiles but fails at runtime".

## Example
```bash
# Add jars or dirs to classpath
java -cp "lib/*:out" com.example.Main
```

## Pitfalls

* Multiple versions of the same library can shadow each other (dependency hell).
* `ClassNotFoundException` vs `NoClassDefFoundError` indicate different failure timing.

## Related

* JVM: JVM uses classpath to find classes.
* Exceptions: missing classes cause runtime exceptions.
* Maven vs Gradle: build tools manage classpath.

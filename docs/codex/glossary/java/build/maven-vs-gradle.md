---
title: Maven vs Gradle
id: glossary/java/build/maven-vs-gradle
world: java
level: beginner
tags: [java, build-tools, dependencies]
related:
  - codex:glossary/java/fundamentals/classpath
  - codex:glossary/java/testing/junit-basics
---

# Maven vs Gradle

## Definition
**Maven** and **Gradle** are Java build tools. Maven is convention-heavy with XML (`pom.xml`); Gradle is scriptable with Groovy/Kotlin (`build.gradle`), often faster and more flexible.

## Usage
- Use Maven for standardized enterprise builds.
- Use Gradle for flexible multi-module builds and custom tasks.
- Both manage dependencies, compile, and run tests.

## Example
```bash
# Maven
mvn test

# Gradle
./gradlew test
```

## Pitfalls

* Dependency conflicts can occur in both; understand transitive deps.
* CI caching differs; be consistent with one tool per project.

## Related

* Classpath: build tools construct the classpath.
* JUnit Basics: build tools run tests.

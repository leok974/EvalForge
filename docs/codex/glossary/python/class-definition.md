---
id: glossary/python/class-definition
title: Class Definition
world: python
level: beginner
tags: [oop, architecture, syntax]
related:
  - codex:glossary/python/instance-method
  - codex:glossary/python/python-function
---

## Definition
A **Class** is a blueprint for creating objects. It bundles data (attributes) and behavior (methods) into a single logical unit. This is the foundation of **Object-Oriented Programming (OOP)**.

## Syntax
```python
class ReactorCore:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.load = 0

    def get_status(self) -> str:
        return f"Load: {self.load}/{self.capacity}"
```

## Why Use Classes?
- **Encapsulation**: Keep related data and logic together.
- **State Management**: Objects maintain their own internal state over time.
- **Reuse**: Create multiple instances (e.g., `core_v1 = ReactorCore(100)`, `core_v2 = ReactorCore(500)`).

## Related
- **Instance Methods**: Functions defined inside a class that act on the instance (`self`).
- **Python Function**: While similar, methods are tied to a specific object context.

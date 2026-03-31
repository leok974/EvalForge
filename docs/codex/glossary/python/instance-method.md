---
id: glossary/python/instance-method
title: Instance Method
world: python
level: beginner
tags: [oop, logic]
related:
  - codex:glossary/python/class-definition
---

## Definition
An **Instance Method** is a function defined inside a class that is intended to be called on an instance of that class. It always takes `self` as its first argument, which refers to the specific object the method is operating on.

## Example
```python
class Tool:
    def __init__(self, name: str):
        self.name = name
        self.active = False

    def toggle(self):
        """This is an instance method."""
        self.active = not self.active
        print(f"{self.name} is now {'ON' if self.active else 'OFF'}")

# Usage
laser = Tool("Plasma Laser")
laser.toggle() # 'self' is automatically passed as 'laser'
```

## Usage in Systems
Methods are used to implement the "Behavior" of system components. For example, a `DatabaseConnection` class might have `connect()`, `query()`, and `close()` methods.

## Related
- **Class Definition**: Where instance methods are housed.
- **Self**: The naming convention for the first argument of an instance method.

---
title: Dependency Injection (DI)
id: codex:glossary/python/systems/dependency-injection
world: python
---

# Dependency Injection

**Dependency Injection (DI)** is a design pattern where an object receives other objects that it depends on (called dependencies) rather than creating them internally.

## Why use DI?

- **Decoupling:** Classes don't need to know how to construct their dependencies.
- **Testing:** Easy to swap real dependencies with mocks.
- **Configurability:** Dependencies can be configured externally.

## Example

**Without DI (Hardcoded):**
```python
class Service:
    def __init__(self):
        self.db = Database() # Hard dependency

    def get_data(self):
        return self.db.query()
```

**With DI:**
```python
class Service:
    def __init__(self, db: Database): # Injected dependency
        self.db = db

    def get_data(self):
        return self.db.query()

# Usage
db = Database()
service = Service(db)
```

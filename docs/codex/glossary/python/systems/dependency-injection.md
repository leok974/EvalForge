---
id: glossary/python/systems/dependency-injection
title: Dependency Injection
world: python
level: intermediate
tags: [architecture, testing, design-patterns]
related:
  - codex:glossary/python/systems/interface
  - codex:glossary/python/systems/separation-of-concerns
  - codex:glossary/python/systems/dependency
---

## Definition
**Dependency injection** is a design pattern where a function or class receives its dependencies as arguments instead of creating them internally. This makes code more testable, flexible, and easier to understand.

## Usage
-Pass dependencies as constructor arguments or function parameters.
- Use dependency injection to swap real implementations with mocks in tests.
- Apply to databases, API clients, and external services.

## Example
```python
# Without DI: hard to test (creates DB connection internally)
class UserService:
    def __init__(self):
        self.db = Database()  # Hard-coded dependency
    
    def get_user(self, user_id):
        return self.db.query(f"SELECT * FROM users WHERE id={user_id}")

# With DI: easy to test (dependency injected)
class UserService:
    def __init__(self, db):
        self.db = db  # Injected
    
    def get_user(self, user_id):
        return self.db.query(f"SELECT * FROM users WHERE id={user_id}")

# In tests, inject a mock
mock_db = MockDatabase()
service = UserService(mock_db)
```

## Pitfalls

* Over-engineering simple code with DI adds unnecessary complexity.
* Not using DI makes testing require complex mocking or actual database connections.

## Related

* Interface: DI works well with abstract interfaces.
* Separation of Concerns: DI helps separate concerns.
* Dependency: DI makes dependencies explicit.
---
id: glossary/python/systems/separation-of-concerns
title: Separation of Concerns
world: python
level: intermediate
tags: [architecture, design-principles, maintainability]
related:
  - codex:glossary/python/systems/dependency-injection
  - codex:glossary/python/systems/interface
  - codex:glossary/python/systems/side-effect
---

## Definition
**Separation of concerns** is a design principle where distinct responsibilities are isolated into separate modules, functions, or classes. Each component should do one thing well and not mix unrelated logic.

## Usage
- Separate business logic from presentation (e.g., don't mix HTML generation with database queries).
- Keep data access, validation, and processing in different layers.
- Use separate functions for I/O, computation, and error handling.

## Example
```python
# Bad: mixed concerns (validation + DB + business logic)
def create_user(name, email):
    if not email or "@" not in email:
        return None
    user = db.insert({"name": name, "email": email})
    send_welcome_email(email)
    return user

# Better: separated concerns
def validate_email(email):
    return email and "@" in email

def save_user(name, email):
    return db.insert({"name": name, "email": email})

def create_user(name, email):
    if not validate_email(email):
        raise ValueError("Invalid email")
    user = save_user(name, email)
    send_welcome_email(email)
    return user
```

## Pitfalls

* Over-separating creates too many tiny functions that are hard to follow.
* Mixing concerns makes code hard to test and maintain.

## Related

* Dependency Injection: DI enforces separation of concerns.
* Interface: interfaces define boundaries between concerns.
* Side Effect: separating side effects is a key concern.
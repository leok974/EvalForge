---
id: fastapi-dependency-injection
title: FastAPI Dependency Injection
world: world-python
tier: 2
difficulty: intermediate
tags: [fastapi, architecture, testing]
summary: >-
  Using the Depends system to manage shared logic, database sessions, and security requirements.
version: 1
last_updated: 2025-11-29
xp_reward: 100
prerequisites: []
stack: [fastapi]
source: curated
trust_level: high
---

# Definition
> TL;DR: FastAPI's Dependency Injection (DI) system lets you declare requirements (like DB sessions or current user) as function parameters, handling setup, teardown, and caching automatically.

# The Golden Path (Best Practice)
Use `Annotated` (Python 3.9+) to keep your route signatures clean and type-safe.

```python
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

# 1. Define the Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 2. Create a Type Alias (Reduces boilerplate)
Database = Annotated[Session, Depends(get_db)]

# 3. Use in Route
@app.get("/items/")
def read_items(db: Database):
    return db.query(Item).all()
```

# Common Pitfalls (Anti-Patterns)

❌ **Manual Instantiation:**

```python
@app.get("/items/")
def read_items():
    db = SessionLocal() # Don't do this!
    # If this errors, the connection might never close.
    return db.query(Item).all()
```

✅ **Why the fix works:**
The `yield` syntax in a dependency acts as a context manager. FastAPI guarantees the code *after* the `yield` runs even if the route throws an error, ensuring connections close.

# Trade-offs

  - ✅ **Testability:** You can override dependencies (mock the DB) via `app.dependency_overrides` without changing route code.
  - ✅ **Scope:** Handles request-scoped lifecycle automatically.
  - ❌ **Magic:** It can be unclear where `db` comes from for new developers.

# Deep Dive (Internals)

FastAPI resolves the dependency graph topologically. If `get_current_user` depends on `get_token`, and `get_token` depends on `oauth2_scheme`, FastAPI builds the chain and executes it in order. It caches the result within a single request scope (unless `use_cache=False`).

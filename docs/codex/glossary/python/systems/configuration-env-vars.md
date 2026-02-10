---
id: glossary/python/systems/configuration-env-vars
title: Configuration & Environment Variables
world: python
level: beginner
tags: [configuration, deployment, security]
related:
  - codex:glossary/python/systems/venv
  - codex:glossary/python/systems/dependency
  - codex:glossary/python/dictionary
---

## Definition
**Environment variables** are key-value pairs set outside your code that configure application behavior (API keys, database URLs, feature flags). They let you change config without modifying code, which is essential for deploying to different environments (dev, staging, prod).

## Usage
- Store secrets (API keys, passwords) in environment variables, not in code.
- Use `os.getenv()` to read environment variables.
- Document required environment variables in README or `.env.example`.

## Example
```python
import os

# Read from environment (with fallback default)
database_url = os.getenv("DATABASE_URL", "sqlite:///default.db")
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY environment variable must be set")

# Set environment variable (bash/terminal)
# export API_KEY="secret123"
# python app.py
```

## Pitfalls

* Hardcoding secrets in code exposes them in version control.
* Forgetting to document required environment variables breaks deployments.

## Related

* Venv: environment variables are often set per virtual environment.
* Dependency: configuration often includes dependency URLs.
* Dictionary: `os.environ` is a dictionary of environment variables.
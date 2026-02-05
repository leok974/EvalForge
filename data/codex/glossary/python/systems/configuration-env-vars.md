---
title: Configuration & Environment Variables
id: codex:glossary/python/systems/configuration-env-vars
world: python
---

# Configuration & Env Vars

Managing configuration separately from code is a core principle of The Twelve-Factor App.

## Environment Variables

Environment variables are key-value pairs stored outside your application code. They allow you to:
- Change behavior between environments (Dev, Staging, Prod) without changing code.
- Keep secrets (API keys, DB passwords) safe.

## Python `os.environ`

In Python, you can access environment variables using `os.environ`:

```python
import os

# Get a value, defaults to None if not set
db_url = os.environ.get("DATABASE_URL")

# Get a value, raises KeyError if not set
secret = os.environ["API_SECRET"]
```

## `.env` Files

For local development, it is common to use a `.env` file to store these variables and load them using libraries like `python-dotenv`.

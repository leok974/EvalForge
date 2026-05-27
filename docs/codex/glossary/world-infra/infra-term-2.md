---
title: Environment & Secrets
id: glossary/world-infra/term-2
world: world-infra
level: intermediate
tags: [configuration, security, secrets]
related:
  - codex:glossary/infra/container
  - codex:glossary/infra/docker-compose
---

# Environment & Secrets

## Definition
Environment variables configure apps without changing code. Secrets are sensitive values (API keys, passwords) that should not be committed to git.

## Usage
- Store secrets in env vars or secret managers.
- Use `.env` for local dev (gitignored).
- Validate required env vars at startup.

## Example
```yaml
services:
  api:
    environment:
      - ENV=prod
      - DATABASE_URL=${DATABASE_URL}
```

## Pitfalls

* Logging secrets by accident is common; scrub logs.
* Missing env vars should fail fast, not silently default.

## Related

* Container: containers receive environment variables.
* Docker Compose: Compose manages environment variables.
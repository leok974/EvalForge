---
title: "Environment & Secrets"
world_id: world-infra
type: codex_entry
level: tier1
---

# Environment & Secrets

Runtime config should come from environment variables.
Secrets should not be committed.

## Env vars
- `PORT`, `MODE`, `DATABASE_URL`, etc.
- Provide safe defaults where appropriate.

## Secrets handling
Tier-1 rule:
- store secrets outside git (env files, CI secret stores)
- fail fast when required secrets are missing

## Tiny patterns
Compose env injection:
- `environment:` inline vars
- `env_file:` load from file

## Common pitfall
“works locally” because you have `.env` but CI/prod doesn’t.
Fix: document required vars + validate at startup.


## Pitfalls

- Exposing sensitive ports in production.
- Hardcoding secrets in the Dockerfile.

## Related

- [[infra/containers]]
- [[infra/docker-compose]]

## Example

``` yaml
version: '3.8'
services:
  app:
    image: alpine
```
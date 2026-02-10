---
title: "Healthchecks & Readiness"
world_id: world-infra
type: codex_entry
level: tier1
---

# Healthchecks & Readiness

A process being alive ≠ a service being ready.

## Healthcheck
Asks: “is it up and responding?”

## Readiness
Asks: “is it ready to serve traffic?” (DB connected, migrations done, etc.)

## Common patterns
- `/health` (cheap, always fast)
- `/ready` (can include dependency probes)

## Tiny guidance
- keep health cheap
- keep readiness informative
- make failures explicit (logs + status codes)


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
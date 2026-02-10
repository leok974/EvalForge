---
title: "Networks"
world_id: world-infra
type: codex_entry
level: tier1
---

# Networks

Containers can talk to each other when they share a network.

## Compose default behavior
Compose creates a default network and connects services.
Then services can reach each other by service name, e.g. `db:5432`.

## Common pitfalls
- services are on different networks
- using localhost instead of service name
- exposing DB ports unnecessarily (keep internal when possible)

## Tiny pattern
In Compose:
- app connects to `postgres://db:5432/...`
not `localhost:5432`


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
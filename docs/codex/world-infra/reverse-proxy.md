---
title: "Reverse Proxy"
world_id: world-infra
type: codex_entry
level: tier1
---

# Reverse Proxy

A reverse proxy sits in front of services to:
- route requests by path/host
- unify URLs
- terminate TLS (often)
- add headers, compression, caching rules

## Typical setup
- proxy listens on 80/443
- routes `/api` to backend
- routes `/` to frontend

## Common pitfalls
- wrong path rewriting (`/api` becomes `//api`)
- websocket/SSE headers not forwarded
- timeouts too low

## Tier-1 mindset
You don’t need “perfect nginx wizardry.”
You need predictable routing + clear debug logs.


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
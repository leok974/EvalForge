---
title: "Debugging Playbook"
world_id: world-infra
type: codex_entry
level: tier1
---

# Debugging Playbook (Stop Guessing)

When something breaks, follow this order.

## 1) Where am I?
Host or container?

## 2) Is the process running?
- check container list
- check service status

## 3) Is it listening on the right port?
- confirm internal port
- confirm host mapping

## 4) Can other services reach it?
- same network?
- using service names, not localhost?

## 5) Is config present?
- env vars exist
- defaults correct
- secrets present where required

## 6) Is it ready?
- healthcheck returns OK
- readiness passes dependency probes

## 7) Read logs around failure
- look at startup logs first
- then failing request logs

## Common “smoking gun” messages
- connection refused → not listening / wrong host
- timeout → wrong route / firewall / proxy
- 500 on ready → dependency not reachable
- 404 on API → proxy rewrite mismatch

## Outcome
At the end, you should have:
- the exact failing command
- the exact error
- the one configuration/routing fix that resolves it


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
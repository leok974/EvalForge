---
title: "Ports & Localhost"
world_id: world-infra
type: codex_entry
level: tier1
---

# Ports & Localhost

This is the #1 infra confusion.

## Localhost depends on where you are
- On your host: `localhost` is your machine.
- Inside a container: `localhost` is that container.

## Port mapping
If a container listens on 8000 internally, expose it to the host:
- `-p 8000:8000` means host 8000 → container 8000

## Common failure modes
- app listens on 127.0.0.1 inside container (not reachable)
- wrong port mapping
- trying to reach host localhost from another container

## Tiny patterns
- listen on all interfaces: `0.0.0.0`
- check ports: `ss -ltnp` (Linux) or service logs

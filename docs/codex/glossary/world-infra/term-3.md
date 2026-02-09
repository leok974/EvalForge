---
title: Debugging Playbook
id: glossary/world-infra/term-3
world: world-infra
level: intermediate
tags: [debugging, troubleshooting, operations]
related:
  - codex:glossary/infra/container
  - codex:glossary/infra/docker-compose
  - codex:glossary/infra/port-mapping
---

# Debugging Playbook

## Definition
A debugging playbook is a repeatable checklist for diagnosing failures: reproduce, isolate, inspect logs, verify config, and fix the smallest thing.

## Usage
- Start with symptoms (error messages, status codes).
- Check health endpoints.
- Verify environment variables and ports.
- Inspect logs and container state.

## Example
```bash
docker compose ps
docker compose logs -f api
curl -fsS http://localhost:8000/api/ready
```

## Pitfalls

* Skipping reproduction leads to guessing.
* Changing many things at once makes it hard to know what fixed it.

## Related

* Container: inspect container logs and state when debugging.
* Docker Compose: Compose commands are central to debugging.
* Port Mapping: verify ports are mapped correctly.
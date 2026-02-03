---
title: "Docker Compose Basics"
world_id: world-infra
type: codex_entry
level: tier1
---

# Docker Compose Basics

Compose runs multiple services together: app + DB + cache + proxy.

## Why it matters
Most real apps are multi-service. Compose makes local stacks reproducible.

## Key concepts
- services: named containers
- networks: shared connectivity between services
- volumes: persistence

## Tiny patterns
- start: `docker compose up -d`
- stop: `docker compose down`
- rebuild: `docker compose up -d --build`
- logs: `docker compose logs -f <service>`

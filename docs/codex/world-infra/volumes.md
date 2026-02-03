---
title: "Volumes"
world_id: world-infra
type: codex_entry
level: tier1
---

# Volumes

Containers have ephemeral filesystems by default.
If the container is removed, its local files are gone.

Volumes provide persistence (DB data, caches, uploads).

## Two common types
- named volumes (managed by Docker)
- bind mounts (map host directory into container)

## Common pitfalls
- forgetting volume for DB → data disappears
- bind mounting entire project and overriding built artifacts (depends on workflow)

## Tiny patterns
- list: `docker volume ls`
- inspect: `docker volume inspect <name>`

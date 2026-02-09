---
title: Filesystem
id: glossary/infra/filesystem
world: infra
level: beginner
tags: [storage, persistence, docker]
related:
  - codex:glossary/infra/permissions
  - codex:glossary/infra/path
---

# Filesystem

## Definition
In containers, the filesystem is usually ephemeral: changes vanish when the container is removed. Persistent data should go in volumes or external storage.

## Usage
- Use volumes for DB data and caches.
- Copy app code into image for immutable deploys.
- Use `.dockerignore` to keep builds small.

## Example
```yaml
services:
  db:
    image: postgres:16
    volumes:
      - db_data:/var/lib/postgresql/data
volumes:
  db_data:
```

## Pitfalls

* Writing data into the container without a volume leads to data loss.
* Permission mismatches happen when UID/GID differs.

## Related

* Permissions: filesystem permissions control access.
* Path: paths navigate the filesystem.
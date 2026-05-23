---
id: glossary/docker/networks-and-volumes
title: Docker Networks and Volumes
world: docker
level: beginner
tags: [docker, networking, volumes, persistence, compose]
related:
  - codex:glossary/docker/layers-and-caching
  - codex:glossary/docker/compose-patterns
---

## Definition

**Networks** control how containers communicate with each other and the outside world. **Volumes** control how data persists beyond the lifetime of a container. Both are first-class objects in Docker Compose.

## Networks

By default, Compose puts all services in a single default bridge network. Any service can reach any other service by its service name as a hostname (e.g. `db`, `api`). Declaring **named networks** gives you finer-grained isolation:

```yaml
networks:
  app_net:           # declared at top level
  admin_net:

services:
  api:
    networks:
      - app_net      # can reach db, cannot reach admin tools
  db:
    networks:
      - app_net
  admin:
    networks:
      - app_net
      - admin_net    # can reach api, db, AND admin tools
```

### Why Named Networks?

* **Isolation** — services on separate networks cannot communicate unless explicitly connected.
* **Security** — your database shouldn't be reachable from the internet-facing proxy.
* **Clarity** — named networks document intent in the Compose file.

## Volumes

Containers are ephemeral — when a container is removed, its filesystem is gone. Volumes persist data independently of any container lifecycle.

### Anonymous vs Named Volumes

```yaml
# Anonymous — Docker manages the name, hard to reference or back up
volumes:
  - /var/lib/postgresql/data

# Named — stable identifier, easy to inspect and back up
volumes:
  - db_data:/var/lib/postgresql/data

# Bind mount — maps a host path into the container (dev-friendly, not for prod)
volumes:
  - ./nginx.conf:/etc/nginx/conf.d/default.conf
```

Named volumes must be declared at the top level:

```yaml
volumes:
  db_data:   # Docker manages the actual storage location
```

### Choosing Volume Type

| Type | Use case |
|---|---|
| Named volume | Database data, user uploads — anything that must survive container restarts |
| Bind mount | Config files, source code during development |
| Anonymous volume | Temporary scratch space (avoid if the data matters) |

## Common Patterns

### Database with Named Volume and Healthcheck

```yaml
services:
  db:
    image: postgres:15
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app_net

volumes:
  db_data:

networks:
  app_net:
```

### Nginx Config via Bind Mount

```yaml
services:
  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    ports:
      - "80:80"
    networks:
      - app_net
```

The `:ro` suffix mounts the file read-only inside the container.

## Pitfalls

* **Exposing the database port to the host** — if `db` is only accessed by other services, don't publish its port. `ports: ["5432:5432"]` on a database is a security risk in production.
* **Using bind mounts for production data** — bind mounts are machine-specific. Named volumes work on any Docker host.
* **Forgetting the top-level `volumes:` key** — Compose requires named volumes to be declared even if the value is `null`:
  ```yaml
  volumes:
    db_data:   # the null value is intentional
  ```

## Related

* Layers and Caching: how Docker builds efficient images.
* Compose Patterns: reference patterns for common multi-service stacks.

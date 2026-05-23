---
id: glossary/docker/compose-patterns
title: Docker Compose Patterns
world: docker
level: intermediate
tags: [docker, compose, healthcheck, depends_on, restart, secrets]
related:
  - codex:glossary/docker/layers-and-caching
  - codex:glossary/docker/networks-and-volumes
---

## Definition

Docker Compose patterns are battle-tested conventions for structuring multi-container applications. The patterns below cover the most common production concerns: startup ordering, resilience, secret management, and three-tier architecture.

## Pattern 1: Healthcheck + Depends-On Chain

Without proper ordering, your API will try to connect to the database before Postgres has finished starting, and crash. The solution is a healthcheck + `condition: service_healthy`:

```yaml
services:
  api:
    image: my-api:latest
    depends_on:
      db:
        condition: service_healthy   # wait for DB to be healthy, not just started

  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

**Without** this pattern, `depends_on: - db` only waits for the container to start — not for Postgres to accept connections.

## Pattern 2: Restart Policies

```yaml
services:
  api:
    restart: unless-stopped   # restart on crash, stop on explicit docker stop
  db:
    restart: unless-stopped
```

| Policy | Behaviour |
|---|---|
| `no` (default) | Never restart |
| `always` | Always restart, including on Docker daemon restart |
| `unless-stopped` | Restart on crash; don't restart if you explicitly stopped it |
| `on-failure` | Restart only on non-zero exit code |

`unless-stopped` is the right default for most production services.

## Pattern 3: Secrets via env_file

Hardcoded credentials in Compose files get committed to Git and leaked. Use `env_file` instead:

```yaml
services:
  db:
    image: postgres:15
    env_file:
      - .env          # loaded from host filesystem, never committed
    environment:
      POSTGRES_DB: app    # non-sensitive config stays inline
```

Your `.env` file (gitignored):
```
POSTGRES_PASSWORD=my-real-secret
DB_PASSWORD=my-real-secret
```

**Rule**: if the value would be dangerous in a leaked commit, it belongs in `.env`.

## Pattern 4: Three-Tier Stack (nginx + api + db)

The canonical production pattern separates concerns into three layers:

```yaml
version: "3.9"
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"                     # only nginx talks to the outside world
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      api:
        condition: service_healthy
    networks:
      - app_net
    restart: unless-stopped

  api:
    build: .
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app_net
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: appdb
    env_file:
      - .env
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app_net
    restart: unless-stopped

volumes:
  db_data:

networks:
  app_net:
```

**Key properties:**
- Only `nginx` exposes a host port. `api` and `db` are internal only.
- All services share `app_net` for service-name DNS resolution.
- `db_data` is a named volume so Postgres data survives container restarts.
- Startup chain: `db` healthy → `api` healthy → `nginx` starts.

## Pattern 5: Multi-Stage Build for the API

Pair your Compose file with a multi-stage Dockerfile to ship a lean image:

```dockerfile
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

## Pitfalls

* **`depends_on` list form in production** — `depends_on: [db]` only waits for container start, not readiness. Always use the long form with `condition: service_healthy` when you have a healthcheck.
* **Exposing the DB port** — `ports: ["5432:5432"]` on `db` makes Postgres reachable from outside Docker. Remove it unless you're debugging locally.
* **No `.dockerignore`** — without `.dockerignore`, `COPY . .` sends `node_modules/`, `.git/`, and other large directories to the daemon on every build.

## Related

* Layers and Caching: how Docker builds images efficiently.
* Networks and Volumes: isolation and persistence in detail.

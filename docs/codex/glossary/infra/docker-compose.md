---
title: Docker Compose
id: glossary/infra/docker-compose
world: infra
level: intermediate
tags: [docker, orchestration, multi-container]
related:
  - codex:glossary/infra/container
---

# Docker Compose

## Definition
**Docker Compose** defines multi-container applications (services, networks, volumes) in one file, so you can run the whole stack consistently.

## Usage
- Define app + db + cache together.
- Create stable internal DNS between services.
- Store shared config in one place.

## Example
```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgres://app:dev@db:5432/app
    depends_on: [db]
  db:
    image: postgres:16
    environment:
      - POSTGRES_PASSWORD=dev
```

## Pitfalls

* `depends_on` doesn't wait for DB readiness; use healthchecks.
* Binding ports unnecessarily exposes services to the host.

## Related

* Container: Compose orchestrates multiple containers.

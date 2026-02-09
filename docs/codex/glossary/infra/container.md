---
title: Container
id: glossary/infra/container
world: infra
level: beginner
tags: [docker, runtime, processes]
related:
  - codex:glossary/infra/image
  - codex:glossary/infra/dockerfile
  - codex:glossary/infra/port-mapping
---

# Container

## Definition
A **container** is a runnable instance of an image: it's a process with its own filesystem view, environment variables, and (usually) isolated networking. Containers are lightweight compared to VMs because they share the host kernel.

## Usage
- Run a service reproducibly (API, DB, worker).
- Inject config via env vars.
- Mount volumes for persistent data.

## Example
```bash
docker run --rm -p 8000:8000 -e ENV=dev my-api:latest
docker ps
docker logs -f <container>
```

## Pitfalls

* Containers are not "mini VMs" — filesystem changes vanish unless persisted (volume).
* Relying on container IPs is brittle; use service DNS in a network.

## Related

* Image: containers are created from images.
* Dockerfile: Dockerfiles define how to build images for containers.
* Port Mapping: port mapping exposes container ports to the host.

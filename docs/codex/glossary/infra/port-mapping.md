---
title: Port Mapping
id: glossary/infra/port-mapping
world: infra
level: beginner
tags: [docker, networking, ports]
related:
  - codex:glossary/infra/container
---

# Port Mapping

## Definition
Port mapping exposes a container port to the host: `hostPort:containerPort`. Example `5173:5173` lets your browser reach a dev server in a container.

## Usage
- Expose only what you need.
- Keep host ports consistent across projects.
- Use internal networks for service-to-service traffic.

## Example
```yaml
services:
  web:
    ports:
      - "5173:5173"
```

## Pitfalls

* Port conflicts are common (`EADDRINUSE`); check what's already listening.
* Binding DB ports to host is often unnecessary and risky.

## Related

* Container: port mapping exposes container ports.

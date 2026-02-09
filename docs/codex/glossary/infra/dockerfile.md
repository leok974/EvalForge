---
title: Dockerfile
id: glossary/infra/dockerfile
world: infra
level: beginner
tags: [docker, build, configuration]
related:
  - codex:glossary/infra/image
  - codex:glossary/infra/filesystem
---

# Dockerfile

## Definition
A **Dockerfile** defines how to build an image: base image, copied files, installed dependencies, and startup command.

## Usage
- Use a small base image.
- Copy only what you need.
- Pin dependency versions when possible.

## Example
```dockerfile
FROM node:20-slim
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY . .
CMD ["node", "server.js"]
```

## Pitfalls

* Copying everything early breaks caching (dependency steps rerun constantly).
* Forgetting `WORKDIR` causes confusing path errors.

## Related

* Image: Dockerfiles build images.
* Filesystem: Dockerfiles define filesystem structure.

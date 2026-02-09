---
title: Image
id: glossary/infra/image
world: infra
level: beginner
tags: [docker, build, deployment]
related:
  - codex:glossary/infra/dockerfile
  - codex:glossary/infra/container
---

# Image

## Definition
An **image** is an immutable template that contains a filesystem snapshot plus metadata (entrypoint, env defaults). Containers are created from images.

## Usage
- Build images from Dockerfiles.
- Tag versions for deploys.
- Push/pull from a registry.

## Example
```bash
docker build -t evalforge-api:dev .
docker tag evalforge-api:dev ghcr.io/org/evalforge-api:dev
docker push ghcr.io/org/evalforge-api:dev
```

## Pitfalls

* "latest" tags are ambiguous; prefer versioned tags.
* Big images slow CI and deploys; use multi-stage builds.

## Related

* Dockerfile: Dockerfiles define how to build images.
* Container: containers are instances of images.

---
title: "Images & Containers"
world_id: world-infra
type: codex_entry
level: tier1
---

# Images & Containers

An **image** is an immutable template.
A **container** is a running instance of that image (a process + filesystem + config).

## Build vs run
- Build creates the image.
- Run starts containers from that image.

## Key idea
If you change files on your host, your running container does not magically update unless you rebuild (or mount a volume).

## Tiny patterns
- build: `docker build -t myapp .`
- run: `docker run --rm -p 8000:8000 myapp`
- list: `docker ps`
- logs: `docker logs <container>`


## Pitfalls

- Exposing sensitive ports in production.
- Hardcoding secrets in the Dockerfile.

## Related

- [[infra/containers]]
- [[infra/docker-compose]]

## Example

``` yaml
version: '3.8'
services:
  app:
    image: alpine
```
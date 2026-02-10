---
title: "Dockerfile Basics"
world_id: world-infra
type: codex_entry
level: tier1
---

# Dockerfile Basics

A Dockerfile describes how to build an image.

## Typical shape
1) choose a base image
2) copy files
3) install deps
4) set command

## Common gotchas
- forgetting to copy needed files
- installing deps before copying manifests (slower builds)
- running as root unnecessarily (advanced hardening later)

## Tiny pattern (Node example)
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
EXPOSE 8000
CMD ["npm","start"]
```


## Pitfalls

- Exposing sensitive ports in production.
- Hardcoding secrets in the Dockerfile.

## Related

- [[infra/containers]]
- [[infra/docker-compose]]
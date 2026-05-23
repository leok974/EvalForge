---
id: glossary/docker/layers-and-caching
title: Docker Layers and Build Cache
world: docker
level: beginner
tags: [docker, layers, caching, build, performance]
related:
  - codex:glossary/docker/networks-and-volumes
  - codex:glossary/docker/compose-patterns
---

## Definition

Every instruction in a Dockerfile creates a **layer** — an immutable, content-addressed snapshot of the filesystem at that point. Docker builds images by stacking these layers. The **build cache** re-uses previously built layers when neither the instruction nor its inputs have changed, making rebuilds fast.

## How Layers Work

Each `RUN`, `COPY`, and `ADD` instruction writes a new layer on top of the previous one:

```
Layer 0: FROM python:3.11-slim       ← base image (pulled once)
Layer 1: WORKDIR /app
Layer 2: COPY requirements.txt .     ← content hash of requirements.txt
Layer 3: RUN pip install -r ...      ← result of install
Layer 4: COPY . .                    ← content hash of your source
Layer 5: CMD ["python", "app.py"]
```

If your source code changes at Layer 4, only Layer 4 and Layer 5 need to be rebuilt. Layers 0–3 are served from cache instantly.

## The Golden Rule: Dependencies Before Source

The most important caching optimisation is to copy slow-changing files (dependency manifests) **before** fast-changing files (source code):

```dockerfile
# Bad — source change invalidates the pip install layer
COPY . .
RUN pip install -r requirements.txt

# Good — pip install layer only rebuilds when requirements.txt changes
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

The same rule applies to `package.json` for Node projects:

```dockerfile
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
```

## Multi-Stage Builds

Multi-stage builds let you keep build tooling out of the final image, dramatically reducing size:

```dockerfile
FROM node:18 AS builder
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build

FROM node:18-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

`COPY --from=builder` pulls files from the `builder` stage without importing its layers. The final image only contains what you explicitly copy.

## Pitfalls

* **`COPY . .` too early** — any source change invalidates all subsequent layers including expensive `RUN pip install` or `RUN npm install` steps.
* **Combining unrelated steps into one `RUN`** — merging unrelated steps prevents granular cache hits. Separate steps that change at different rates.
* **`--no-cache`** in CI without good reason — forces a full rebuild every time, negating all caching benefits.
* **Large build context** — everything in the build context is sent to the Docker daemon on every build. Use `.dockerignore` to exclude `node_modules/`, `.git/`, and other large directories.

## Related

* Networks and Volumes: how services communicate and persist data at runtime.
* Compose Patterns: orchestrate multi-container apps with Compose.

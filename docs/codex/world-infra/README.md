---
title: "World Infra — Codex"
world_id: world-infra
type: codex_landing
version: 1
---

# World Infra — Codex (Toolchain & Deployment Foundations)

This Codex is the **map + debugger** for infra concepts you’ll use across [oaicite:0]{index=0}: containers, networks, configuration, health, and production sanity.

If Git is “version control confidence,” Infra is “environment confidence.”

---

## How to use this Codex

- **Learning mode:** read the Core Model once, then follow the Quest Map.
- **Stuck mode:** jump to the specific tool (ports, networks, env, health checks).
- **Panic mode:** run the Debug Checklist and don’t guess.

---

## Core Model (the 80/20)

### 1) Build vs Run
- **Build** creates an image (immutable template).
- **Run** starts a container (a process + filesystem + config).

Read: [images-and-containers](./images-and-containers.md)

### 2) Networking is explicit
“localhost” means different things depending on where you are (host vs container).
Ports must be mapped; services must share a network.

Read: [ports-and-localhost](./ports-and-localhost.md), [networks](./networks.md)

### 3) Configuration is external
Runtime config should come from environment variables and secrets.
Defaults must be safe.

Read: [env-and-secrets](./env-and-secrets.md)

### 4) Reliability needs health checks
A service being “up” isn’t the same as “ready.”
Health checks + readiness probes prevent flaky systems.

Read: [healthchecks](./healthchecks.md)

### 5) Production adds a front door
Reverse proxies route traffic, terminate TLS, and unify URLs.

Read: [reverse-proxy](./reverse-proxy.md)

---

## Quick Links

- [images-and-containers](./images-and-containers.md)
- [dockerfile-basics](./dockerfile-basics.md)
- [compose-basics](./compose-basics.md)
- [ports-and-localhost](./ports-and-localhost.md)
- [networks](./networks.md)
- [volumes](./volumes.md)
- [env-and-secrets](./env-and-secrets.md)
- [healthchecks](./healthchecks.md)
- [reverse-proxy](./reverse-proxy.md)
- [ci-basics](./ci-basics.md)
- [observability](./observability.md)
- [debugging-playbook](./debugging-playbook.md)

---

## Quest Map (by skill)

### Container basics
- What an image/container is → [images-and-containers](./images-and-containers.md)
- Build a minimal image → [dockerfile-basics](./dockerfile-basics.md)

### Local orchestration
- Multiple services + wiring → [compose-basics](./compose-basics.md)
- Storage persistence → [volumes](./volumes.md)

### Networking
- Ports + “localhost confusion” → [ports-and-localhost](./ports-and-localhost.md)
- Container networking basics → [networks](./networks.md)

### Configuration & safety
- Env vars & secrets → [env-and-secrets](./env-and-secrets.md)
- Health/readiness checks → [healthchecks](./healthchecks.md)

### Production shape
- Reverse proxy patterns → [reverse-proxy](./reverse-proxy.md)
- CI sanity gates → [ci-basics](./ci-basics.md)

### Operate & debug
- Logs/metrics basics → [observability](./observability.md)
- “It’s broken” workflow → [debugging-playbook](./debugging-playbook.md)

---

## Debug Checklist (when something is broken)

1) **Am I in host or container?** (don’t assume)
2) **Is the process running?**
3) **Is the service listening on the expected port?**
4) **Are ports mapped correctly?**
5) **Are services on the same network?**
6) **Is config present (env/secrets)?**
7) **Is the service ready (health/readiness)?**
8) **What do logs say right before failure?**
9) **Can I reproduce with a single command?**
10) **What changed since last working state?**

See: [debugging-playbook](./debugging-playbook.md)

---
id: boss-reactor-core-infra
title: BOSS – Reactor Core Meltdown
world: world-infra
tier: 2
tags: [boss, infra, docker, health-checks, grid]
summary: A timed ops encounter that stress-tests your ability to keep services healthy under pressure.
related_quests: [inf_boss]
---

# Definition

**Reactor Core Meltdown** is an Infra World boss fight that simulates a full-scale outage in **The Grid**.

In narrative terms, the **Core Reactor** is unstable. In technical terms, your **services are misconfigured**: containers restart, health checks fail, and traffic can't reach the right upstreams.

Defeating this boss means restoring **operational stability** under a strict time limit.

---

# Encounter Overview

> **World:** The Grid (Infra)  
> **Boss ID:** `reactor_core`  
> **Difficulty Profile:** `normal` → `hard` (health check + routing + resilience)  
> **Timer:** 30 minutes (real-time)  
> **Primary Skills:** Docker, Compose, health checks, networking, observability.

During the encounter:

- A **Boss HUD** appears with a countdown, HP bar, and score.
- You receive a mission briefing from **KAI** (the Operator).
- You are given a broken (or incomplete) infra scenario (e.g. a failing `docker-compose.yml`, a miswired `nginx` proxy, or a missing health check).
- You must repair the configuration and submit a solution **before the timer hits zero**.

The **Judge (ZERO)** evaluates your fix using a rubric and returns a `boss_result` that affects your **System Integrity (HP)** and XP.

---

# The Golden Path (Winning Strategy)

To consistently defeat Reactor Core, you need a disciplined approach to infra debugging:

1. **Read the Symptoms, Not Just the Code**
   - Check logs: `docker compose logs`, health endpoints (`/ready`, `/healthz`), and connection errors.
   - Identify *where* the failure is: DNS, port mismatch, health check, env vars, or startup order.

2. **Stabilize the Core (Health Checks First)**
   - Ensure each critical service (API, DB, Redis, etc.) has:
     - A **startup command** that actually runs the server.
     - A **health endpoint** that can be probed.
     - A **Compose `healthcheck`** or platform-level check pointing at that endpoint.

3. **Restore the Grid (Networking & Routing)**
   - Verify **service names** and **ports** line up across:
     - `docker-compose.yml` services
     - Any reverse proxies (nginx, traefik)
     - Environment variables (e.g. `API_BASE_URL`, `DATABASE_URL`).
   - Prefer **service names** (`backend`, `db`) over `localhost` inside the Compose network.

4. **Harden for Load (Resilience)**
   - Check restart policies (`restart: unless-stopped` / `on-failure` where appropriate).
   - Avoid blocking startup with long migrations if they're not required for readiness.
   - Make sure **readiness checks** reflect "can serve traffic" not "boot finished once."

5. **Verify End-to-End**
   - Rebuild / restart (`docker compose up --build`) and hit:
     - `/ready` or `/healthz` on the backend
     - Frontend → API calls through the proxy
   - Only submit once the system behaves like the mission expects.

---

# Common Pitfalls (How the Reactor Explodes)

❌ **Symptom chasing without a hypothesis**  
Randomly changing ports, env vars, or image tags without understanding the actual failure mode.

✅ Instead: Form a mental model:
> "Frontend → nginx → backend:8000 → db:5432. Where is the chain breaking?"

---

❌ **Using `localhost` inside Docker networks**  
Containers trying to talk to `localhost:8000` instead of `backend:8000`.

✅ Instead: Use **service names** defined in `docker-compose.yml`:
```yaml
services:
  web:
    environment:
      - API_URL=http://backend:8000
```

---

❌ **No health checks, only wishes**  
Relying on "the container started" instead of explicit readiness.

✅ Instead: Add targeted checks:

```yaml
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/ready"]
      interval: 10s
      timeout: 3s
      retries: 5
```

---

❌ **Tight coupling of migrations and readiness**  
Blocking the server from starting until heavy migrations complete, causing health checks to time out.

✅ Instead:
- Run migrations as a separate step (init container / script).
- Keep readiness focused on "API is responsive."

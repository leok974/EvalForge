---
slug: boss-containment-grid-strategy
boss_id: containment_grid
tier: 3
world_id: world-grid
tags:
  - boss
  - containment_grid
  - strategy
  - infra
  - docker
title: "The Containment Grid – Strategy & Survival Guide"
---

> ELARA: "Infra is just contracts written in YAML."

## Strategy Highlights

1. **Draw the Topology**

- List every service: web, api, db, redis, etc.
- For each, note:
  - What it depends on,
  - Which ports it should expose (internally + externally),
  - Required env vars.

Think in diagrams first, YAML second.

2. **Name Things Consistently**

- Service name in compose = hostname in URLs.
- Ports: expose only what needs to be public; internal traffic should use container ports & hostnames.

3. **Stabilize Healthchecks**

- Use simple, robust endpoints (`/healthz`, `/ready`).
- Reasonable intervals and `start_period`.
- Avoid false negatives during startup (DB migrations, cold caches).

4. **Treat Env as a Contract**

- Define required env vars in one place.
- Provide sensible defaults in dev.
- Never silently fall back to broken values.

The Containment Grid rewards infra that is **predictable, observable, and documented**, not "it worked once on my laptop."

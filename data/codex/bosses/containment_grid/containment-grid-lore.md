---
slug: boss-containment-grid-lore
boss_id: containment_grid
tier: 1
world_id: world-grid
tags:
  - boss
  - containment_grid
  - lore
  - infra
  - docker
title: "The Containment Grid – System Briefing"
---

> KAI: "If the Grid fails, nothing else boots."

## Narrative Brief

The **Containment Grid** is the first major boss of **THE GRID (world-infra)**.

In-universe, it’s the infrastructure layer that keeps services:

- Containerized,
- Networked,
- Routed,
- Healthy.

Your task: take a **broken docker-compose + env configuration** and make the stack start reliably.

**What this boss is testing:**

- Understanding of **service dependencies** (DB before API before web).
- Correct use of **ports, networks, and environment variables**.
- Healthcheck sanity and restart policies.

The Grid is where "it runs on my machine" stops being an excuse.

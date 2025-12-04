---
slug: boss-containment-grid-attacks
boss_id: containment_grid
tier: 2
world_id: world-grid
tags:
  - boss
  - containment_grid
  - attacks
  - infra
  - docker
title: "The Containment Grid – Failure Modes & Misconfigurations"
---

> ZERO: "Most outages are misconfig, not code."

## Attack Patterns

1. **Port Clash – "Overload Channel"**  
   - API and web both try to bind the same host port.
   - Test checks: one of them fails to start.

2. **Wrong Hostname – "Ghost Upstream"**  
   - Web depends on `api:8000` but docker-compose uses a different service name or port.
   - Test checks: health endpoint 502/connection refused.

3. **Missing Env – "Silent Void"**  
   - Critical env var (DB URL, secret, base URL) is missing or mis-typed.
   - Test checks: app logs crash or fails health ping.

4. **Healthcheck Loop – "Flapping Cage"**  
   - Healthcheck is misconfigured (bad path, wrong interval).
   - Test checks: container constantly restarting.

5. **Network Isolation – "Partition"**  
   - Services on different networks, or DNS disabled.
   - Test checks: ping/requests fail across containers.

The boss ensures you can read a compose file like a wiring diagram, not like a magic incantation.

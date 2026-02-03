---
title: "Observability (Logs/Metrics)"
world_id: world-infra
type: codex_entry
level: tier1
---

# Observability (Logs/Metrics)

If you can’t see it, you can’t fix it.

## Logs (minimum)
- startup logs (port, mode)
- request logs (path, status)
- error logs (message + context)

## Metrics (next)
- request count
- error count
- latency buckets

## Tier-1 standard
- logs should explain why readiness failed
- errors should include enough context to reproduce

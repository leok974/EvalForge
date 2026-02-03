---
title: "Observability"
world_id: world-node
type: codex_entry
level: tier1
---

# Observability

Observability means you can answer:
- What happened?
- Why did it happen?
- How often does it happen?

Start simple: **logs first**, then metrics, then tracing.

---

## Logs (the minimum)
Good logs tell you:
- which path ran
- key inputs (safe ones)
- error details on failure

Pattern:
```js
console.log("server_start", { port });
console.error("request_error", { message: err.message });
```

---

## Metrics (next step)

Metrics are counts/timers:

* requests_total
* errors_total
* latency_ms

Even without a full metrics system, thinking in counters helps.

---

## Tracing (advanced)

Tracing tracks a request across components.
You won’t need it for most Tier-1 quests, but you will later in Infra/Agents.

---

## EvalForge guidance

For quests:

* don’t spam logs unless allowed
* log only when it helps debugging
* keep stdout/stderr behavior consistent with tests

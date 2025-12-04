---
codex_id: boss-applylens-runtime-attacks
kind: boss-attacks
boss_slug: applylens-runtime-boss
world_id: world-projects
project_slug: applylens
tier: 2
title: The Inbox Maelstrom — Attack Patterns
---

# The Inbox Maelstrom — Attack Patterns

The Maelstrom does not attack with a single move.  
It escalates through **waves** of failure modes that often look "normal" in isolation.

## Phase 1 — Backlog Swell

**Move: "Drizzle to Downpour"**

- A moderate but sustained stream of Gmail messages.
- Backfill jobs and webhook deliveries overlap.
- Latency climbs slowly, then suddenly.

**Symptoms:**

- Worker queue depth rising.
- Occasional timeouts to Gmail or the DB.
- Logs show sporadic `Retrying...` but no hard failures yet.

## Phase 2 — Index Churn

**Move: "Shard Choke"**

- Elasticsearch becomes the bottleneck.
- Indexing slows or fails intermittently.
- Read path is "fine" while write path is in pain.

**Symptoms:**

- Documents stuck in "ingested to DB" but "missing in search".
- Increased indexing error rate (4xx/5xx from ES).
- User-facing search results lag behind the true inbox state.

## Phase 3 — Retry Storm

**Move: "Echo Flood"**

- Retries trigger aggressively without proper backoff.
- A single flaky dependency causes **amplified traffic**.
- Duplicate work saturates workers and queues.

**Symptoms:**

- Same messages processed multiple times.
- Correlated spikes in CPU, DB connections, and ES requests.
- Logs full of repeating error + retry cycles.

## Phase 4 — Silent Degradation

**Move: "Quiet Drown"**

- The system no longer crashes — it just "kind of works".
- Some messages never make it to the Tracker.
- Alerts are missing or overly permissive.

**Symptoms:**

- Users notice "missing" applications.
- Metrics look noisy but do not clearly signal violation.
- No single stack trace explains what went wrong.

The Maelstrom thrives in the **gaps**:

- No clear ingest latency SLO.
- No metric connecting "new Gmail threads" to "new Tracker rows".
- No single dashboard where you can see the pipeline end-to-end.

Understanding these attack patterns is the first step to beating this boss.

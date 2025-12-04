---
id: boss-applylens-runtime-attacks
title: The Inbox Maelstrom – Attack Patterns
boss_slug: applylens-runtime-boss
tier: 2
world_id: world-projects
project_slug: applylens
tags:
  - boss
  - attacks
  - runtime
  - ingest
---

The Inbox Maelstrom doesn't attack with claws or lasers. It attacks with **surges**, **delays**, and **silence**.

Here are its main patterns.

---

## 1. Surge of Threads

**Pattern:** A sudden burst of new Gmail messages and threads.

**Symptoms**

- Ingest queues back up.
- Workers are always busy.
- Latency from email arrival → indexed search grows steadily.

**Weak Presentations**

- Workers have no backpressure or queue visibility.
- No per-step timing metrics (e.g. Gmail fetch vs DB write vs index).
- Logs show errors but without thread IDs or correlation IDs.

The Maelstrom thrives when you can't **see** the backlog and don't know how long work is taking.

---

## 2. Flaky Dependencies

**Pattern:** Intermittent failures in Gmail, Postgres, or Elasticsearch.

**Variants**

1. **Gmail hiccups**
   - Occasional timeouts or 500s from Gmail API.
   - Webhooks arriving late or in bursts.

2. **Database stumbles**
   - Transient connection errors.
   - Slow inserts/updates during peak load.

3. **Search strain**
   - Indexing fails for some documents.
   - Cluster temporarily unavailable.

**Weak Presentations**

- No retries or only naive retries (hammering failing dependencies).
- Missing timeout configuration (requests hanging forever).
- Failure paths that log but do not surface metrics.

The Maelstrom loves systems that assume every dependency is always up.

---

## 3. Silent Poison

**Pattern:** Partial success that looks fine until it isn't.

Examples:

- Email body stored, but attachments or labels silently ignored.
- DB record written, but search index never updated.
- Index updated, but with a corrupted or truncated document.

**Weak Presentations**

- No invariants like "thread in DB must also be in index".
- No sanity checks on counts (e.g., threads ingested vs threads searched).
- No alerts tied to error ratios or missing records.

The Maelstrom wins if the system _appears_ healthy while data is slowly drifting out of sync.

---

## 4. Backfill vs. Real-Time Collision

**Pattern:** Backfill jobs and real-time ingest step on each other.

**Symptoms**

- Duplicate threads.
- Out-of-order updates.
- Race conditions between historical imports and latest messages.

**Weak Presentations**

- No idempotency keys or deduplication logic.
- Last-write-wins behavior with no notion of "freshness".
- Backfill jobs that don't respect current load.

The Maelstrom exploits any ambiguity in which event should "win".

---

## 5. Observability Blackout

**Pattern:** Everything is "fine" until someone notices it's not.

**Symptoms**

- Latency SLOs silently violated.
- Ingest is "working" but new messages don't appear in search.
- Dashboards show broad CPU/memory, but nothing about ingest health.

**Weak Presentations**

- No ingest-specific metrics:
  - `ingest_latency_seconds`
  - `ingest_errors_total`
  - `ingest_queue_depth`
- Logs are unstructured or missing key context (email ID, thread ID, user ID).

The Maelstrom feasts in darkness. If you don't measure it, you can't defend against it.

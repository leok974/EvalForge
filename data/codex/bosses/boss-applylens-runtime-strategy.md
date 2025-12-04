---
id: boss-applylens-runtime-strategy
title: The Inbox Maelstrom – Strategy Guide
boss_slug: applylens-runtime-boss
tier: 3
world_id: world-projects
project_slug: applylens
tags:
  - boss
  - strategy
  - runtime
  - ingest
---

This guide assumes you already understand:

- How Gmail messages move through ApplyLens (Tier 1).
- The Maelstrom's main attack patterns (Tier 2).

Now we focus on **how to win**.

---

## 1. Define the Win Condition

Before you fight, decide what "victory" looks like in concrete terms.

Examples for ApplyLens runtime:

- **Latency SLO**
  - "95% of emails ingested and indexed within 2 minutes of arrival."

- **Error Budget**
  - "Ingest error rate < 1% over a storm window."

- **Consistency Guards**
  - "Every thread in the DB reaches the index within X minutes or is flagged."

Make these conditions **machine-checkable**:
- Metrics.
- Alerts.
- Automated checks in your boss rubric.

---

## 2. Make the Path Observable

Turn the ingest pipeline into a series of **visible stages**:

1. Gmail → "received" event
2. Worker dequeues job
3. DB write succeeds
4. Index write succeeds
5. Search-ready status

For each stage, add:

- A **counter** (events processed).
- A **latency histogram** (per stage and end-to-end).
- Logs that include:
  - `thread_id`
  - `user_id`
  - `source` (webhook/backfill)
  - `attempt` or `retry_count`

If you can't quickly answer "where is this thread stuck?", you're fighting blind.

---

## 3. Engineer for Failure, Not Perfection

Add **structured failure handling**:

- **Timeouts**:
  - Explicit timeouts for Gmail API calls and Elasticsearch operations.
- **Retries with backoff**:
  - Use bounded retries with exponential backoff.
  - Tag retries in logs/metrics (`retry=true`, `retry_count`).
- **Dead-letter or quarantine**:
  - Keep a place for "messages we couldn't ingest yet" with reasons.

In the rubric for the Maelstrom boss, reward:

- Presence of timeouts and backoff.
- Differentiation between "temporary" vs "permanent" failures.
- Clear metrics for retries and dead-letter counts.

---

## 4. Enforce Idempotency and Ordering

The Maelstrom will send duplicates and out-of-order events.

Your defenses:

- **Idempotent writes**:
  - Use thread IDs and message IDs as natural keys.
  - Upserts instead of blind inserts.
- **Last-write-wins with awareness**:
  - Make sure you know _which_ event "wins" (e.g. latest timestamp).
- **Backfill-safe logic**:
  - Backfills should respect the same rules and not overwrite newer state.

In ApplyLens, that means:

- Designing the DB schema and ingest logic so backfills can't clobber recent updates.
- Ensuring Gmail webhook events and backfills converge on the same final state.

---

## 5. Protect the Index

Search is where users feel the Maelstrom most.

Strategy:

- Treat the index as a **derived view** of the DB.
- Make index writes:
  - **Idempotent** (replay-safe).
  - **Checkable** (e.g., "count of indexed threads per user").
- Consider a repair or reconciliation job:
  - Periodically compare DB vs index and re-enqueue missing docs.

If the Maelstrom knocks out your index temporarily, you should be able to heal it without guessing.

---

## 6. Close the Loop with Alerts and Dashboards

A prepared Maelstrom fight uses:

- **Dashboards** that show:
  - Ingest throughput.
  - Latency (per stage + end-to-end).
  - Error + retry rates.
  - Queue depth / backlog.
- **Alerts** tied directly to your win condition:
  - "95th percentile ingest latency > 2 minutes over 10m window."
  - "Ingest error rate > 1% over 5m window."
  - "Index drift detected between DB and search."

For the boss rubric:

- Score higher when:
  - SLOs are explicitly defined and wired to metrics.
  - Alerts are actionable, not just noise.
  - Dashboards make it obvious "where the pain is".

---

## 7. Practice the Storm

Finally, simulate the Maelstrom:

- Run a load script that:
  - Creates a burst of synthetic emails/threads.
  - Mixes normal and pathological examples.
- Watch:
  - Queues.
  - Latencies.
  - Error spikes.
  - Logs for any "unknown" failure modes.

Your goal is not to eliminate chaos entirely.

It's to prove that ApplyLens remains **predictable**, **observable**, and **repairable** when the inbox turns into a storm.

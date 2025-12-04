---
codex_id: boss-applylens-runtime-strategy
kind: boss-strategy
boss_slug: applylens-runtime-boss
world_id: world-projects
project_slug: applylens
tier: 3
title: The Inbox Maelstrom — Strategy Guide
---

# The Inbox Maelstrom — Strategy Guide

The Inbox Maelstrom tests one thing above all:

> Can ApplyLens ingest a surge of emails **quickly, safely, and observably**?

To win this fight, treat it like designing a **defensible ingest SLO** and instrumenting everything around it.

---

## 1. Draw the Pipeline Explicitly

Write this down, ideally in code comments and docs:

1. Gmail → webhook/backfill handler.
2. Handler → worker/queue.
3. Worker → DB (normalized entities).
4. DB → Elasticsearch index.
5. Elasticsearch → UI (Tracker/Search).

For each hop, ask:

- **Where do we log success/failure?**
- **What metrics exist (latency, error rate, throughput)?**
- **What happens on error — drop, retry, or dead-letter?**

If you cannot answer these, the Maelstrom already has an advantage.

---

## 2. Define and Enforce an Ingest SLO

Pick a realistic SLO, for example:

- "95% of new Gmail threads become searchable applications in **under 2 minutes**."

Then:

- Emit a metric like `applylens_ingest_latency_seconds`.
- Include labels such as `source=webhook|backfill`, `status=success|error`.
- Add a simple **SLO check** (even a script or dashboard panel) that shows:
  - SLO window (e.g., last 1h / 24h).
  - Current success vs. budget.

Your boss rubric should **refer to this SLO**, not just raw pass/fail.

---

## 3. Tame the Retry Storm

For every retrying component (webhooks, workers, ES indexing):

- Use **bounded retries with backoff** (e.g., exponential with jitter).
- Make retries **idempotent**:
  - Use stable message IDs.
  - Protect against duplicate rows in DB.
  - Upsert into ES instead of blind insert where possible.

Emit metrics like:

- `applylens_ingest_retries_total`
- `applylens_ingest_dead_letters_total`

The Maelstrom loves unbounded, unobserved retries. Don't give it that.

---

## 4. Guard Elasticsearch as a First-Class Dependency

Treat ES as part of the boss arena:

- Add **indexing latency** and **indexing error** metrics.
- Make sure partial failures are visible:
  - If DB writes succeed but ES indexing fails, log & metric that explicitly.
- Consider a simple dashboard with:
  - New emails per minute.
  - New DB rows per minute.
  - New indexed docs per minute.
  - A simple ratio: `indexed/docs` vs `expected`.

If ES is down or impaired, you should know **before** users do.

---

## 5. Build a "Maelstrom Drill" Scenario

Add a test or script that simulates:

- A batch of N Gmail messages arriving quickly.
- Expected time for them to reach:
  - DB
  - ES
  - UI

Your boss implementation can:

- Generate synthetic events into the ingest path.
- Measure real latency & error metrics.
- Fail the encounter if:
  - Latency exceeds your SLO.
  - Error rate exceeds 1%.
  - Observability signals are missing.

**Winning the fight** means:

- SLO is defined.
- Metrics and logs prove you're inside the SLO window.
- Retries are controlled, idempotent, and observable.

Once you can reliably pass your Maelstrom drill, the boss becomes a formality.

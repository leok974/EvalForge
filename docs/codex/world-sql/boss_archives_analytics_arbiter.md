# Boss Codex – Archives Analytics Arbiter

- **Boss ID:** `boss-archives-analytics-arbiter`
- **World:** `world-sql` – The Archives
- **Track:** `archives-senior-analytics-architect`
- **Stage:** 3 – Senior Analytics Architect
- **Title:** Archives Analytics Arbiter
- **Tier:** Senior Boss (Legendary)

---

## Lore

Deep in The Archives lies a hall of dashboards and metric definitions, some trusted, some cursed.

Here rules the **Archives Analytics Arbiter** — guardian of **“one source of truth”** that has survived:

- dashboards built directly on raw tables,
- silently broken ETL jobs,
- schema “quick fixes” that corrupt historical numbers,
- metrics whose definitions change every quarter.

It does not care if your SQL is clever. It cares whether teams can **trust the numbers** when it matters.

---

## Attacks

### 1. The Metric Mirage

- **Symptom:** Three dashboards show three different “active users” counts.
- **What it tests:**
  - Quality of metric definitions and grain.
  - Separation of canonical tables vs ad-hoc queries.
  - How schema design prevents ambiguity.

---

### 2. The Slow-Crawl Query

- **Symptom:** A key dashboard times out whenever the CEO opens it.
- **What it tests:**
  - Partitioning and clustering strategy.
  - Indexing and pruning the working set.
  - Understanding of scan patterns and query plans.

---

### 3. The Silent Corruption

- **Symptom:** A pipeline change silently doubles revenue in one country.
- **What it tests:**
  - Data quality tests and checks.
  - Guardrails on schema and transformation changes.
  - Alerting and rollback strategies.

---

### 4. The Broken Lineage

- **Symptom:** No one can answer “where does this number come from?”
- **What it tests:**
  - Lineage capture (from raw to mart).
  - Ownership and documentation for critical tables.
  - Deprecation and migration patterns.

---

### 5. The Nightly Incident

- **Symptom:** A nightly load fails; half the dashboards are stale.
- **What it tests:**
  - Incident debugging runbooks.
  - Reprocessing and backfill strategies.
  - Communication and blast-radius control.

---

## Strategy

To defeat the Archives Analytics Arbiter, the player must submit:

> **“Analytics Architecture Blueprint – Archives Analytics Arbiter”**

A markdown blueprint describing how a real analytics warehouse should be designed and run.

It should cover:

1. **Schemas & grain**
   - Fact and dimension tables with clear grain.
   - Keys and relationships.
   - Which tables are canonical vs exploratory.

2. **Performance & scaling**
   - Partitioning, clustering, and indexing strategies.
   - How to keep dashboard queries predictable at scale.
   - Patterns to avoid (anti-patterns and their fixes).

3. **Quality & testing**
   - Data tests (nulls, uniqueness, referential integrity).
   - Thresholds and anomaly detection.
   - How tests block or gate deploys.

4. **Lineage & governance**
   - How lineage is tracked (tools, conventions, or both).
   - Who owns which tables and metrics.
   - How you evolve schemas and metrics safely over time.

5. **Incidents & recovery**
   - How failures are detected and triaged.
   - How you roll back or re-run loads.
   - How you keep downstream consumers informed and safe.

---

## Boss Fight Shape

- **Submission Format:** markdown with recommended sections:

  - `## Domain & Requirements`
  - `## Core Schemas & Grain`
  - `## Performance & Scaling`
  - `## Quality & Tests`
  - `## Lineage & Governance`
  - `## Incidents & Recovery`
  - `## Rollout & Adoption`

The Arbiter doesn’t require specific tools (dbt vs custom, BigQuery vs Snowflake).  
It wants a design that is **coherent, resilient, and auditable**.

# Boss Codex – Archive Query Warden

- **Boss ID:** `boss-archives-query-warden`
- **World:** `world-sql` – The Archives
- **Track:** `archives-retrieval-analytics`
- **Stage:** `stage-1-archives-retrieval`
- **Title:** Archive Query Warden
- **Tier:** Retrieval & Analytics Boss (Stage 1 Capstone)

---

## Lore

The Archives contain every event, order, and anomaly your systems have ever seen.

At the gate stands the **Archive Query Warden**.

It has watched engineers:

- ship dashboards with double-counted users,
- join on the wrong keys and miss entire regions,
- full-scan tables with billions of rows during peak traffic,
- “fix” reports by changing the chart instead of the query.

To pass, you must show you can **interrogate the Archives with precision**:

- translate a vague metric request into a concrete query,
- reason about joins, filters, and time windows,
- debug correctness and performance issues,
- and leave behind a runbook another analyst can trust.

---

## Attacks

### 1. Phantom Growth

- **Symptom:** DAU or revenue looks higher than it really is.
- **In game:** The Warden shows a metric that spiked after a query change.
- **What it tests:** Understanding of DISTINCT vs COUNT, grain of measurement, and double-counting via joins.

---

### 2. Silent Drop

- **Symptom:** Some segments “disappear” from reports.
- **In game:** A WHERE or JOIN condition quietly filters out nulls/regions/timezones.
- **What it tests:** Null handling, outer vs inner joins, and filter placement.

---

### 3. Time Warp

- **Symptom:** Dashboards disagree on “yesterday’s” data.
- **In game:** The Warden uses mismatched time zones and event timestamps.
- **What it tests:** Time windowing, truncation, time zone awareness.

---

### 4. Full-Scan Avalanche

- **Symptom:** Queries become very slow as data grows.
- **In game:** A naive query does table scans on large fact tables.
- **What it tests:** Indexing, partitioning, and query plan reading.

---

## Strategy

To defeat the Archive Query Warden, the player must demonstrate:

1. **Requirement Translation**
   - Turn business questions into precise metric definitions (grain, filters, time window).
   - Identify the correct tables and join paths.

2. **Query Correctness**
   - Construct SQL that matches the intended metric.
   - Handle joins, nulls, and duplicate rows explicitly.

3. **Performance Awareness**
   - Read and respond to query plans (EXPLAIN).
   - Propose indexes/partitions or query rewrites to avoid full scans.

4. **Runbook Mindset**
   - Write a clear, copy-paste-safe investigation and remediation plan.
   - Document assumptions and validation checks.

---

## Boss Fight Shape

- **Submission Format:** A markdown **“Analytics Query Incident Runbook”** with sections:

  - `## Incident Context`
  - `## Phase 1 – Clarify the Metric`
  - `## Phase 2 – Inspect Current Query & Data`
  - `## Phase 3 – Propose Corrected Query`
  - `## Phase 4 – Performance & Safety Checks`
  - `## Phase 5 – Rollout & Monitoring`

- **Scenario (for the player):**

  - You own an analytics query for **daily active users and revenue by country**.
  - A recent change to the query made the numbers:
    - **Too high** for some countries,
    - **Missing** for others,
    - And **much slower** overall.

  - Tables (conceptually):
    - `events` (user_id, event_type, event_ts, country_code)
    - `orders` (order_id, user_id, amount, currency, created_at, country_code)
    - `countries` (country_code, region, is_active)

  The runbook should:

  - Clarify the correct metric definition,
  - Diagnose how the current query is wrong,
  - Propose a fixed query (or family of queries),
  - Improve performance while preserving correctness,
  - Describe validation steps before shipping to production dashboards.

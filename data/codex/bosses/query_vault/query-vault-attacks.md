---
slug: boss-query-vault-attacks
boss_id: query_vault
tier: 2
world_id: world-archives
tags:
  - boss
  - query_vault
  - attacks
  - sql
title: "The Query Vault – Attack Patterns & Failure Modes"
---

> ZERO: "Queries don't 'just work'. They fail silently. That is the problem."

Once you've lost a few times, the Vault begins leaking patterns.

---

## 1. Phantom Growth – "Double Count"

**What it does:**

Creates data with **one-to-many joins**:

- A `user` with many `sessions`,
- A `session` with many `events`,
- A `plan` with multiple pricing changes.

**What it’s testing:**

- Do you know how to avoid counting the same entity multiple times?
- Do you group at the **right level**?

**Typical failures:**

- Summing revenue on a table where rows are already aggregated.
- Joining `payments` to `events` and multiplying amounts.
- Grouping by too many columns, making metrics look smaller than they should.

---

## 2. Null Horizon – "Sparse Keys"

**What it does:**

Populates tables with:

- Users that never activated,
- Events missing `user_id`,
- Payments without associated `plan` rows yet.

**What it’s testing:**

- Do you choose the right join types (`LEFT` vs `INNER`)?
- Do you decide intentionally what to do with **missing relationships**?

**Typical failures:**

- Dropping non-activated users entirely, skewing activation rates.
- Treating missing data as zeros without explicit logic.
- Misinterpreting NULL timestamps.

---

## 3. Time Warp – "Window Drift"

**What it does:**

Creates **off-by-one** time windows:

- Events that happen just outside the intended query range.
- Late-arriving data.

**What it’s testing:**

- Do you define time windows precisely (`>=` vs `>`, `<` vs `<=`)?
- Do you anchor metrics correctly to event or user creation timestamps?

**Typical failures:**

- Including data outside the requested period.
- Splitting a single sequence across multiple windows.
- Using server-local time assumptions where UTC is required.

---

## 4. Filter Fog – "Hidden Conditions"

**What it does:**

Requires metrics under **specific constraints**:

- Only paying users,
- Only active plans,
- Only certain event types.

**What it’s testing:**

- Do you correctly apply filters at the proper stage?
- Do you filter in the **subquery**, not just in the outer query?

**Typical failures:**

- Aggregating everything, then filtering, leading to wrong denominators.
- Applying filters after grouping and mislabeling segments.

---

### Summary

If your queries:

- Use correct joins and grouping levels,
- Treat **NULL** and missing relationships deliberately,
- Define time windows sharply,

…the Query Vault opens. Otherwise, it returns pretty, **confidently wrong** answers.

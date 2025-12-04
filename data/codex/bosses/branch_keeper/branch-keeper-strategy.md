---
slug: boss-branch-keeper-strategy
boss_id: branch_keeper
tier: 3
world_id: world-timeline
tags:
  - boss
  - branch_keeper
  - strategy
  - git
title: "The Branch Keeper – Strategy & Survival Guide"
---

> ELARA: "Good Git skill is just 'never panic plus a plan.'"

Strategy:

1. **State First, Commands Second**

- Identify:
  - HEAD branch,
  - Upstream state,
  - Local changes,
  - Relationship between branches (ahead/behind/diverged).

2. **Pick a Sync Model**

- Small, local branches: rebase onto main.
- Long-lived, shared branches: merge with clear messages.

3. **Make Conflicts Explicit**

- Name the files likely to conflict.
- Outline steps:
  - `git fetch`,
  - `git checkout feature`,
  - `git rebase origin/main` (or `merge`),
  - Resolve conflicts,
  - `git push --force-with-lease` or merge back.

The Branch Keeper rewards **calm, explicit plans** that respect teammates and history.

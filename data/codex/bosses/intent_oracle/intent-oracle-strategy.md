---
slug: boss-intent-oracle-strategy
boss_id: intent_oracle
tier: 3
world_id: world-oracle
tags:
  - boss
  - intent_oracle
  - strategy
  - agents
title: "The Intent Oracle – Strategy & Survival Guide"
---

> ELARA: "A good agent is mostly a good planner."

Key strategy:

1. **Normalize Goals**

- Extract:
  - Objective (what to accomplish),
  - Constraints (what not to do),
  - Inputs (what we already know),
  - Outputs (what we must produce).

2. **Design a Typed Plan**

- Plan is an array of steps:
  - `tool`, `input`, `success_condition`, optional `rollback`.

3. **Filter Tools by Capability + Safety**

- Only pick tools that:
  - Can actually help,
  - Are allowed under guardrails.

4. **Prefer Read → Decide → Write**

- Read state (queries),
- Decide (reason),
- Write (mutations / side effects).

The Intent Oracle rewards planners that **do the minimum safe thing** in a clearly structured way.

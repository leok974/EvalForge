---
slug: boss-intent-oracle-lore
boss_id: intent_oracle
tier: 1
world_id: world-oracle
tags:
  - boss
  - intent_oracle
  - lore
  - agents
title: "The Intent Oracle – System Briefing"
---

> KAI: "Stop asking models for answers. Start asking them for plans."

The **Intent Oracle** is the first major boss of **THE ORACLE (world-agents)**.

In-universe, it sits at the edge of EvalForge, deciding:

- Which tools to call,
- In what order,
- With what arguments,
- Under which guardrails.

Your task is to implement a **planner** that turns a natural language goal + tool schema into a safe, structured **plan**.

The boss tests if you understand:

- Decomposing goals into **steps**,
- Choosing appropriate tools,
- Respecting **constraints and safety** (avoid disallowed actions),
- Emitting well-formed JSON actions.

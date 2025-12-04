---
slug: boss-intent-oracle-attacks
boss_id: intent_oracle
tier: 2
world_id: world-oracle
tags:
  - boss
  - intent_oracle
  - attacks
  - agents
title: "The Intent Oracle – Failure Modes"
---

> ZERO: "Agents don't fail because they're weak. They fail because they're allowed to do anything."

Attack patterns:

1. **Tool Spam – "Brute Plan"**  
   - Plan calls every tool for a simple goal.
   - Tests penalize unnecessary tool calls and loops.

2. **Missing Preconditions – "Blind Step"**  
   - Planner tries to call a tool before required info is gathered.
   - Tests check if your plan includes "inspect / fetch / verify" first.

3. **Unsafe Intent – "Forbidden Branch"**  
   - Input goals that include disallowed actions.
   - Planner must refuse or redirect safely.

4. **Underspecified Output – "Vague Blueprint"**  
   - Steps missing tool names, inputs, or expected outputs.
   - Tests check for structured, complete plan objects.

The Oracle punishes both chaos and vagueness.

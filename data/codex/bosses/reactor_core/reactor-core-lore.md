---
slug: boss-reactor-core-lore
boss_id: reactor_core
tier: 1
world_id: world-python
tags:
  - boss
  - reactor_core
  - lore
  - python
  - backend
title: "The Reactor Core – System Briefing"
---

> KAI: "Operative, you’ve reached the heart of the Foundry. This isn’t a quiz. This is a systems check."

## Narrative Brief

The **Reactor Core** is the first major boss of **THE FOUNDRY (world-python)**.  
It represents a real backend service under pressure: inputs coming from everywhere, strict expectations, and no room for brittle hacks.

In-universe, the Reactor Core powers the entire EvalForge Arcade. Every quest you’ve cleared so far was running on spare batteries and simulator nodes. The boss fight is the moment we connect you to the live bus and see if your code survives.

**What this boss is testing:**

- Can you **design a small, clean API** that does exactly what it says?
- Can you handle **unhappy paths** without falling apart?
- Can you write code that **survives grading**, not just the example in the prompt?

## The Shape of the Fight

You are given:

- A **problem spec** (what the Reactor needs from your code).
- **Starting code** that is intentionally incomplete and slightly suspicious.
- A hidden **rubric** that JudgeAgent (ZERO) uses to grade your submission.

You will face:

- A stream of **test inputs** (normal, edge, and hostile).
- **Time pressure**, simulated via boss HP and attempts.
- **Integrity damage** when your code fails in critical ways.

## Why It Matters

Beating the Reactor Core means you can:

- Take a text spec and turn it into a **robust Python implementation**.
- Respect contracts: function signatures, return types, error handling.
- Think about **systems**, not just lines of code.

This is the boss that separates:

- “I can follow a tutorial”
- from
- “I can build a small, **production-minded** Python service.”

## Intel From Previous Units

> ZERO: "Most Units underestimate the Core. They code for the 'happy path' and then complain about damage."

Common patterns from earlier attempts:

- Forgetting to handle **empty / null / malformed inputs**.
- Ignoring **performance constraints** and timing out.
- Logging nothing useful, so failures are **opaque**.
- Passing tests locally but failing on **grading edge cases**.

Defeat is expected. Learning from the wreckage is mandatory.

---
slug: boss-signal-prism-lore
boss_id: signal_prism
tier: 1
world_id: world-prism
tags:
  - boss
  - signal_prism
  - lore
  - javascript
  - typescript
title: "The Signal Prism – System Briefing"
---

> KAI: "Welcome to the Prism console. These lights aren't decoration. They're telemetry."

## Narrative Brief

The **Signal Prism** is the first major boss of **THE PRISM (world-js)**.

In-universe, it sits between dozens of subsystems:

- UI components emitting interaction events,
- network clients firing requests and responses,
- system watchers broadcasting errors and status.

Everything routes through one structure: the **Signal Panel**.  
Your job is to tame that chaos with a clean, deterministic reducer.

**What this boss is testing:**

- Can you transform a **noisy event stream** into a stable **state representation**?
- Can you write a pure, well-typed **computeSignalPanel** function in TypeScript?
- Can you reason about **ordering, duplicates, and edge cases** without being told every test up front?

## The Shape of the Fight

You are given:

- A TypeScript signature for `SignalEvent` and `SignalState`.
- A starting stub for `computeSignalPanel(events: SignalEvent[]): SignalState[]`.
- A hidden rubric that scores your implementation.

You will face:

- Streams that are mostly sorted by `ts`… but not always.
- Duplicate events (same id/kind/ts) that must not explode the state.
- Partial payloads (`severity`, `message`) sprinkled inconsistently across events.

## Why It Matters

The Signal Prism simulates real front-end infra problems:

- Turning **logs + events** into a **view model**.
- Designing reducers that can handle **a weekend's worth of weirdness**.
- Keeping the code simple enough that Future You (or another engineer) can debug it.

If The Foundry taught you to build a backend function,  
The Prism asks: **can you maintain coherent UI state when the world is messy?**

## Intel From Previous Units

> ZERO: "Units tend to overfit to ‘the example stream’ and then panic when events arrive out of order."

Common failure modes:

- Assuming events are always strictly ordered by `ts`.
- Ignoring duplicates and accidentally duplicating signals.
- Mutating input arrays or reusing mutable objects in multiple places.
- Returning different shapes depending on the path (sometimes missing fields).

Defeat is expected. Turning chaos into a clean reducer is the actual training.

---
codex_id: boss-applylens-agent-attacks
kind: boss-attacks
boss_slug: applylens-agent-boss
world_id: world-projects
project_slug: applylens
tier: 2
title: The Intent Oracle — Attack Patterns
---

# The Intent Oracle — Attack Patterns

The Intent Oracle does not brute-force the system.  
It attacks your **assumptions** about how smart, safe, and consistent your agents are.

## Pattern 1 — Ambiguous Threads

**Move: "Schrödinger's Application"**

- A thread looks partly like a job lead, partly like marketing content.
- Subject lines are vague (e.g., "Quick question").
- The model must infer intent from subtle cues (sender, previous replies, links).

**Symptoms:**

- Misclassification into generic categories (e.g., "Other" or "Newsletter").
- No suggested action when one is clearly needed (e.g., follow-up, reply).
- Over-reliance on subject line without reading the body.

---

## Pattern 2 — Tool Drift

**Move: "Silent Misalignment"**

- Tools (search, profile lookup, trackers) evolve over time.
- The agent's prompts and expectations **do not**.

**Symptoms:**

- Tools return partial or newly structured responses.
- The agent mis-parses tool output or assumes fields that no longer exist.
- Failures appear as subtle behavioral changes, not obvious errors.

---

## Pattern 3 — Evaluation Mirage

**Move: "False Confidence"**

- The eval harness has only "clean" examples.
- Benchmarks match the training data too closely.

**Symptoms:**

- High scores on curated test data.
- Poor performance on real production threads.
- No clear measurement of regressions when prompts/models change.

---

## Pattern 4 — Safety and Budget Erosion

**Move: "The Whispered Overspend"**

- The agent occasionally chains too many tool calls or model invocations.
- The cost of triaging certain threads quietly creeps up.

**Symptoms:**

- No per-thread cost metric.
- No per-run guardrails (max tool calls, max tokens).
- Surprising spikes in monthly LLM bills.

The Intent Oracle punishes:

- Weak or non-existent eval loops.
- Poorly defined success criteria.
- Uninstrumented decisions.

It rewards systems where **behavior can be measured, compared, and improved over time**.

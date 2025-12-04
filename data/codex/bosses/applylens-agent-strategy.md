---
codex_id: boss-applylens-agent-strategy
kind: boss-strategy
boss_slug: applylens-agent-boss
world_id: world-projects
project_slug: applylens
tier: 3
title: The Intent Oracle — Strategy Guide
---

# The Intent Oracle — Strategy Guide

The Intent Oracle boss asks a hard question:

> "Can you prove your triage agent is accurate, stable, and cost-aware — not just impressive in demos?"

To defeat this boss, build a **real evaluation loop** and wire it into ApplyLens.

---

## 1. Define Explicit Success Criteria

Before you tweak prompts or tools, write down:

- Target **classification labels** (e.g., "New Opportunity", "Follow-up", "Rejection", "Noise").
- For each label, what **action** the system should propose.
- Acceptable **error rates** (e.g., missed opportunities ≤ 5%, false positives ≤ 3%).

Your rubrics and eval harness should refer directly to these targets.

---

## 2. Build a Small But Honest Benchmark

Curate a dataset of email threads that:

- Reflect real-world messiness:
  - Recruiter spam.
  - Ambiguous "checking in" messages.
  - Genuine new roles with subtle differences.
- Include "hard" examples where humans could disagree.

Store ground truth as:

- `thread_id`
- `expected_label`
- `expected_action`
- Optional notes explaining why.

Even 30–50 carefully chosen examples can be enough to stress the system.

---

## 3. Implement the Judge & Coach Loop

Your evaluation harness should:

1. Run the triage agent on each benchmark thread.
2. Compare predicted labels/actions to ground truth.
3. Call a **Judge** (LLM or rule-based) to:
   - Assign a score.
   - Explain discrepancies.
4. Optionally invoke a **Coach** agent to propose prompt/tool changes.

Log for each run:

- Accuracy / F1 per label.
- Confusion matrix (what is misclassified as what).
- Structured "failure mode" tags (e.g., `overconfident`, `missed_attachment`, `company_alias`).

The Intent Oracle boss should **consume these logs** and score the encounter.

---

## 4. Add Guardrails and Budgets

For each triage call:

- Cap the number of tool calls.
- Cap the max tokens.
- Track cost per decision (even if only approximate).

Emit metrics like:

- `applylens_agent_triage_tokens_total`
- `applylens_agent_triage_cost_usd_total`
- `applylens_agent_triage_failures_total`

The boss should detect:

- Runs where cost explodes.
- Runs where guardrails are ignored or bypassed.

---

## 5. Wire the Eval Loop Into the Boss Fight

When you "fight" The Intent Oracle:

- The boss scenario should trigger a full benchmark run.
- Results should be summarized as:
  - Overall score (0–100).
  - Key failure modes.
  - Cost vs. budget.

Consider boss victory criteria like:

- Accuracy ≥ target threshold (e.g., 90% on critical labels).
- No hard safety violations (e.g., sending a reply where we should not).
- Cost within defined per-thread or per-run budget.

If you implement this well, the boss not only tests your agent —  
it also becomes a **regression gate** for future changes to prompts, models, and tools.

Beating The Intent Oracle means you have:

- A living benchmark.
- A Judge/Coach loop.
- Real telemetry around agent behavior.

At that point, you're not just "using LLMs" —  
you're **operating** an intelligent system with the same discipline as any other production service.

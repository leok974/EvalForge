---
id: boss-applylens-agent-strategy
title: The Intent Oracle – Strategy Guide
boss_slug: applylens-agent-boss
tier: 3
world_id: world-projects
project_slug: applylens
tags:
  - boss
  - strategy
  - agents
  - llm
---

To defeat the Intent Oracle, you must treat ApplyLens's agent layer as an **evaluated system**, not just a clever prompt.

This guide assumes you've already:

- Mapped the agent tools and flows (Tier 1).
- Understood the Oracle's attack patterns (Tier 2).

---

## 1. Define Intent Taxonomy and Outcomes

Start by making the agent's job **explicit**.

Examples of intents for ApplyLens:

- `interview_invite`
- `offer`
- `rejection`
- `application_update`
- `networking`
- `marketing`
- `security_alert`
- `other`

For each intent, define:

- What the **suggested actions** are (e.g., "create Tracker row", "schedule interview reminder", "flag as risky").
- What **never** should be suggested (e.g., do not reply automatically to security alerts).

This taxonomy becomes the backbone of your boss rubric.

---

## 2. Build a Small but Sharp Benchmark

You don't need thousands of examples to start.

Create a curated set of email threads:

- 5–10 examples for each high-impact intent.
- Several **ambiguous** cases where classification is genuinely hard.
- A handful of **adversarial** examples (spammy recruiters, phishing attempts, noisy newsletters).

For each example, annotate:

- The **true intent**.
- The **acceptable suggestions**.
- Any **hard constraints** (e.g., "never mark this as harmless").

Store this set in a format the eval harness can consume (JSON, DB, or files).

---

## 3. Implement Judge & Coach

Your Agent Boss rubric should be powered by a **Judge/Coach** pattern:

- **Judge**
  - Given an email + the agent's output, score:
    - Intent correctness.
    - Suggestion quality.
    - Policy/safety adherence.
  - Emit a structured score (e.g., 0–100) and a list of failure reasons.

- **Coach**
  - Given the same context, propose improvements:
    - Better intent label.
    - Safer/more useful suggestions.
    - Prompt or tool selection changes.

Wire this into a runner such as:

```text
agent_eval_runner:
  - Loads benchmark threads.
  - Runs the agent on each.
  - Invokes Judge/Coach.
  - Aggregates scores and failure modes.
```

The boss fight should use these scores directly: **HP damage = eval performance**.

---

## 4. Make Uncertainty First-Class

The Oracle is dangerous when it's overconfident.

Add explicit handling for **uncertainty**:

- Allow the agent to say "uncertain" or "needs review".
- Use confidence thresholds:
  - High-confidence → show suggestion.
  - Medium → show with caution/badge.
  - Low → route to human with "needs review" label.

In prompts and tools:

- Ask the model to estimate its own confidence qualitatively (low/medium/high).
- Encode rules:
  - "If confidence is low, prefer a safe fallback rather than a strong suggestion."

In the boss rubric:

- Penalize **overconfident wrong answers** more than humble "I'm unsure" when appropriate.

---

## 5. Guardrails and Policies

Before you let the Oracle roam:

- Define a **policy layer**:
  - Forbidden actions (e.g., never send emails automatically).
  - Sensitive patterns (e.g., security alerts, financial info, identity docs).

- Enforce:
  - Pre-classify risky threads (using heuristics or a separate risk model).
  - Restrict what suggestions are allowed on high-risk content.

In the code:

- Centralize these rules rather than scattering them across prompts.
- Make it easy to update policy without rewriting the whole agent.

In the boss fight:

- The rubric should check that high-risk examples are treated conservatively.

---

## 6. Track Performance Over Time

The Oracle boss isn't just a one-off fight. It's a **season**.

Put these in place:

- **Metrics**
  - `agent_suggestion_accuracy` on the benchmark set.
  - `agent_suggestions_total` vs `accepted` vs `rejected_by_user`.
  - `agent_policy_violations_total` (should be ~0).

- **Dashboards**
  - Intent distribution over time.
  - Accuracy by intent type.
  - Top failure reasons from the Judge.

- **Change Protocol**
  - When you change prompts, tools, or models:
    - Re-run the eval harness.
    - Compare scores.
    - Only promote if performance is stable or improved.

The boss rubric should reward:

- Having a repeatable eval process.
- Logging and surfacing regressions.
- Keeping a healthy safety margin on high-risk intents.

---

## 7. Accept That You'll Be Wrong, Then Learn

You will never reach 100% accuracy.

Victory against the Intent Oracle is not "never making mistakes"; it is:

- Making **fewer serious mistakes** over time.
- Making it easy to see **where** you're wrong and **why**.
- Turning every correction and failure into a data point for future improvement.

When ApplyLens's triage agent can:

- Explain its reasoning,
- Be evaluated systematically,
- Improve without guesswork,

then the Intent Oracle stops being a threat…

…and becomes a partner.

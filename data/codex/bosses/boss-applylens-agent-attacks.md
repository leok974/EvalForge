---
id: boss-applylens-agent-attacks
title: The Intent Oracle – Attack Patterns
boss_slug: applylens-agent-boss
tier: 2
world_id: world-projects
project_slug: applylens
tags:
  - boss
  - attacks
  - agents
  - llm
---

The Intent Oracle doesn't attack with load. It attacks with **ambiguity**.

---

## 1. Subtle Misclassification

**Pattern:** Emails that look similar but have very different consequences.

Examples:

- Genuine recruiter outreach vs marketing "opportunities".
- Auto-acknowledge vs actual rejection.
- Generic "follow up" vs explicit "action required".

**Weak Presentations**

- One-size-fits-all classification labels.
- No distinction between "low confidence guess" and "high confidence decision".
- No mechanism to learn from corrections.

The Oracle loves edge cases where the cost of being wrong is high.

---

## 2. Over-Confident Suggestions

**Pattern:** The agent acts like it knows more than it does.

Examples:

- Suggesting aggressive follow-up on automated HR spam.
- Marking a critical security email as "promo".
- Recommending replies with inaccurate summaries.

**Weak Presentations**

- No notion of uncertainty or confidence thresholds.
- Suggestions appear equally "strong" regardless of evidence.
- No channel for the user to mark suggestions as harmful or wrong.

The Oracle gains strength every time a user mistakes confidence for correctness.

---

## 3. Tool Misuse and Overspending

**Pattern:** The agent calls tools too often or in the wrong context.

Examples:

- Calling a summarization tool for every message, even trivial ones.
- Hitting vector search for simple inbox filters.
- Ignoring budgets or rate limits.

**Weak Presentations**

- No budgets for tokens or tool calls.
- No distinction between cheap heuristics and expensive LLM passes.
- No tracking of cost vs benefit.

The Oracle exploits any system that says "yes" to every tool invocation.

---

## 4. Evaluation Blind Spots

**Pattern:** The agent is never asked to justify or prove itself.

Examples:

- No benchmark set of labeled email threads.
- No Judge/Coach pair to score decisions.
- No tracking of long-term performance.

**Weak Presentations**

- Relying purely on "vibes" (it feels smart).
- No metrics on suggestion accuracy or user adoption.
- No concept of "regressions" when prompts/models change.

The Oracle thrives in environments where nobody checks the scoreboard.

---

## 5. Safety and Policy Violations

**Pattern:** Suggestions that violate basic user safety or policy constraints.

Examples:

- Suggesting replies that overshare personal information.
- Ignoring "do not contact" tags.
- Misclassifying phishing or suspicious messages as safe.

**Weak Presentations**

- No coarse filters for security or risk.
- No escalation path for ambiguous or dangerous content.
- No clear "do not cross" policies encoded in prompts/tools.

The Oracle will happily walk off a cliff if you never tell it where the edge is.

# World: Agents — Student Guide

Welcome to the Agents world. You’re going to learn how to build systems that can **plan, act, verify, and improve**—without causing chaos.

This world is about engineering discipline: “agentic” does not mean “wild.”

---

## What you’re learning

You will learn to:
- Design a reliable **agent loop**
- Define **tool contracts** that prevent ambiguity
- Add a **verifier** that catches failures early
- Use **approvals/diffs** so actions are safe
- Store **memory** in a way that helps (not hurts)
- Enforce **budgets** so systems don’t spiral
- Add **observability** so you can debug runs

---

## The agent loop (the core pattern)

**Plan → Act → Verify → Report → Iterate**

- **Plan:** break the goal into small steps with expected outputs.
- **Act:** execute steps using tools (not imagination).
- **Verify:** prove that the step worked (tests, checks, queries).
- **Report:** summarize what changed + evidence.
- **Iterate:** continue until goal is satisfied or budget is exceeded.

If a system skips verification, it’s not an agent — it’s a guesser.

---

## Your default safety settings (EvalForge style)

- **Dry-run first** (generate diffs, don’t apply)
- **Restricted tools** (allowlist what can run)
- **Budgeted retries** (no infinite loops)
- **Proof-required merges** (tests must pass)
- **Artifact logging** (every step is recorded)

---

## How EvalForge expects you to work

When you implement agent features or quests, you should be able to answer:

1) **What was the goal?**
2) **What tools were used?**
3) **What changed? (diff or artifact)**
4) **How did we verify?**
5) **How do we rollback?**

This is the difference between “cool demo” and “production-worthy.”

---

## Common failure modes (and what to do)

### 1) “It keeps trying the same thing”
Cause: no clear stop condition.  
Fix: add budgets + stuck detection (max attempts, max steps).

### 2) “It changed the wrong files”
Cause: scope not constrained.  
Fix: allowlist paths, diff-only proposals, denylist patterns.

### 3) “It said it worked but it didn’t”
Cause: no verification.  
Fix: add tests or deterministic checks; never accept “looks good.”

### 4) “It hallucinated APIs or facts”
Cause: missing grounding.  
Fix: require citations from files/tool outputs; add “show your work.”

### 5) “It’s too expensive”
Cause: overusing the main model.  
Fix: split roles: cheap planner/extractor, strong verifier only when needed.

---

## Debug checklist (use this when stuck)

- Is the goal written as a **testable outcome**?
- Do tools return **structured outputs**?
- Is verification **independent** of the generator?
- Is there a **budget** for retries/steps?
- Are changes **diffed + approved** before apply?
- Can you explain failure with **logs + artifacts**?

---

## “A+ agent run” template

**Goal:** …  
**Plan:** 1) … 2) … 3) …  
**Actions:** tool calls + outputs (recorded)  
**Verification:** tests/checks + results  
**Outcome:** what changed + why  
**Rollback:** how to revert safely  
**Next:** follow-ups or remaining risks

---

## Where this world connects

You’ll reuse these patterns in:
- Node and Infra worlds (deployment, health checks, automation)
- Git world (diffs, rollback, safe merges)
- Projects (EvalForge QA, SiteAgent tasks, ApplyLens workflows)

Agents are the glue. The discipline is the product.

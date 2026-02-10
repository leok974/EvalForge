# World: Agents — Codex Hub

This hub explains the **agent loop** used across EvalForge worlds and projects: a system that can plan, call tools, verify outcomes, and act safely.

If you only read one page, read **Agent Loop** first.

---

## Mental model (1 minute)

An **agent** is software that can:
1) **Understand** a goal,
2) **Plan** steps,
3) **Use tools** (files, HTTP, DB, shell, etc.),
4) **Verify** results,
5) **Report** what happened,
6) Repeat until done.

Agents are powerful because they can do **multi-step work**, but they’re dangerous if they act without guardrails. EvalForge’s stance: **safe-by-default**.

---

## The 5 invariants (EvalForge standard)

1) **Contracts are explicit**  
   Inputs/outputs are typed (JSON when possible), tool schemas are documented.

2) **Verification is mandatory**  
   “I ran it” is not proof. We verify via tests, queries, checksums, diff inspection, or independent signals.

3) **Unsafe actions require approval**  
   Anything destructive (delete, deploy, commit, spend money) is gated and reversible.

4) **Budgets exist**  
   Time, tokens, tool calls, retries, and cost are capped. Agents should fail fast when stuck.

5) **Observability is built-in**  
   Every run produces logs, steps, artifacts, and a final report.

---

## Quick links

- [Agent Loop](./agent-loop.md)
- [Prompts & Contracts](./prompts-and-contracts.md)
- [Tool Contracts](./tool-contracts.md)
- [Planner](./planner.md)
- [Executor](./executor.md)
- [Verifier](./verifier.md)
- [Approvals & Diffs](./approvals-and-diffs.md)
- [Memory](./memory.md)
- [Budgets & Rate Limits](./budgets-and-rate-limits.md)
- [Observability & Tracing](./observability-and-tracing.md)
- [Guardrails & Safety](./guardrails-and-safety.md)
- [Grounding & RAG](./grounding-and-rag.md)

---

## Recovery moves (when the agent is failing)

**Symptom: loops / stuck**
- Reduce goal scope to one step
- Add a deterministic verification check
- Add a strict budget for retries (e.g., max 2 attempts)
- Force “report-only” mode

**Symptom: wrong edits**
- Switch to diff-only proposals
- Require tests before applying changes
- Add allowlist paths and forbidden patterns

**Symptom: hallucinating facts**
- Add grounding step: cite sources or inspect files
- Use tool output as truth, not model guesses

**Symptom: slow / expensive**
- Cache intermediate artifacts
- Batch tool calls
- Use smaller models for planning or extraction

---

## What “good” looks like

A good agent run produces:
- A clear plan (steps and expected outputs)
- Tool calls with recorded inputs/outputs
- Verification proof (tests/checks/diffs)
- A concise report: what changed, why, how to undo


## Pitfalls

- Premature optimization can lead to complex, unmaintainable code.
- Ignoring error handling can lead to silent failures.

## Related

- [[general/clean-code]]
- [[general/debugging]]

## Example

``` typescript
const example = () => {
  console.log('Hello');
};
```
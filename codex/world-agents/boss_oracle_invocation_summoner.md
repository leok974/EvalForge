# Boss Codex – Oracle Invocation Summoner

- **Boss ID:** `boss-oracle-invocation-summoner`
- **World:** `world-agents` – The Oracle
- **Track:** `oracle-invocation-circuit`
- **Stage:** `stage-1-oracle-invocation`
- **Title:** Invocation Summoner
- **Tier:** Invocation Boss (Stage 1 Capstone)

---

## Lore

The Oracle hears countless requests every cycle.

Some are clear. Many are not.  
Most arrive as vague wishes: “help me with my inbox”, “fix my pipeline”, “summarize this”, “debug that”.

The **Invocation Summoner** is the guardian of *how* those wishes are turned into **concrete actions**.

It has no patience for:
- prompts that try to do everything in one shot,
- agents that spam tools without a plan,
- or pipelines that can’t explain what they just did.

To pass, you must show that you can translate messy user intent into a **clean, tool-aware invocation design**.

---

## Attacks

The Summoner attacks by exposing classic agent failure modes.

### 1. Intent Blur

- **Symptom:** User asks multi-part questions; the agent treats them as one blob.
- **In game:** The boss presents requests that mix “search, compute, and summarize” and watches if your plan decomposes them.
- **What it tests:** Task decomposition and explicit step planning.

---

### 2. Tool Flail

- **Symptom:** Agent spam-calls tools or calls the wrong tool for a subtask.
- **In game:** The boss shows traces where tools are called redundantly or in the wrong order.
- **What it tests:** Well-modeled tool contracts and clear invocation rules.

---

### 3. Ungrounded Claims

- **Symptom:** Agent answers confidently without consulting the right tools or sources.
- **In game:** The boss injects queries that *require* external data (search/DB) and checks whether your design insists on grounding before answering.
- **What it tests:** Grounding strategy and “when to call tools” logic.

---

### 4. Silent Runes

- **Symptom:** No logs, no metrics, no way to debug.
- **In game:** The boss simulates a failing run and asks, “How would anyone know what happened?”
- **What it tests:** Observability: traces, logs, and guardrails for live runs.

---

## Strategy

To defeat the Invocation Summoner, the player must demonstrate:

1. **Task Modeling & Decomposition**
   - Breaks a messy, real-world request into ordered steps.
   - Identifies which steps are purely reasoning and which need tools.
   - Expresses this as a mini-state-machine or plan.

2. **Tool Contracts & Invocation Logic**
   - Defines a small set of tools with clear inputs/outputs.
   - Specifies when each tool should be called and how outputs feed into the next step.
   - Avoids tool flailing (no pointless calls; no missing obvious calls).

3. **Grounding & Safety**
   - Makes it hard for the agent to hallucinate when tools are available.
   - Encodes policies like “must use search for anything time-sensitive or external”.
   - Handles tool errors and partial results gracefully.

4. **Explainability & Observability**
   - Includes logging/telemetry hooks: what gets logged, where, and why.
   - Describes how to debug a bad run or misrouted tool call.
   - Keeps the design small enough to be maintainable by other engineers.

---

## Boss Fight Shape

- **Submission Format:** A markdown **“Invocation Blueprint”** with these sections:

  - `## Scenario`
  - `## Tools`
  - `## Orchestrator Flow`
  - `## Guardrails & Grounding`
  - `## Observability & Debugging`

- **Scenario (for the boss):**

  A **Research Assistant Agent** that helps an engineer answer technical questions about their codebase and system, using three tools:

  - `repo_search(query)` – semantic/file search over a code repo.
  - `doc_search(query)` – search over architecture / runbook docs.
  - `metrics_query(query)` – query recent metrics/alerts in a monitoring system.

- **Your job as a player:**

  - Design the prompts, tool contracts, and orchestrator flow for this agent.
  - Show how it handles mixed questions like:
    - “Why is latency up on /api/search after the last deploy? Show me relevant code and dashboard views.”
  - Explain how it stays grounded, safe, and debuggable.

The Judge will score your blueprint on:

- **How well you model tasks & substeps,**
- **How clearly you define tool contracts & call logic,**
- **How robustly you handle grounding & safety,**
- **How well another engineer could read and implement your design.**

# Boss Codex – Oracle Orchestrator Prime

- **Boss ID:** `boss-oracle-orchestrator-prime`
- **World:** `world-agents` – The Oracle
- **Track:** `oracle-senior-orchestrator`
- **Stage:** 3 – Senior Orchestrator
- **Title:** Oracle Orchestrator Prime
- **Tier:** Senior Boss (Legendary)

---

## Lore

In the depths of the Oracle’s chamber, simple single-agent prompts are no longer enough.

Here lives the **Oracle Orchestrator Prime** — a mind that thinks in *graphs*, not calls. It coordinates planners, tool specialists, critics, and safety sentinels across dozens of steps and tools.

It has seen:

- agents calling tools with ambiguous contracts,
- infinite reasoning loops with no stop condition,
- “smart” agents that bypass safety policies,
- systems with impressive demos and zero observability.

To pass, you must prove you can design a **multi-agent orchestrator** that is:

- understandable,
- safe,
- observable,
- and evolvable.

---

## Attacks

### 1. The Tool Tangle

- **Symptom:** Tools have vaguely defined inputs/outputs. Agents “just call” them with free-form JSON.
- **What it tests:**
  - Tool contract design and typing
  - Error handling and timeouts
  - How you keep agents from misusing tools

---

### 2. The Runaway Chain

- **Symptom:** A planner agent keeps decomposing tasks, spawning calls until tokens or time run out.
- **What it tests:**
  - Step limits, stop conditions, and budgets
  - Recovery from partial progress
  - How the orchestrator decides to stop or fall back

---

### 3. The Policy Hole

- **Symptom:** Some agents follow safety policy; others “forget”. Sensitive actions slip through side channels.
- **What it tests:**
  - Central policy layer vs per-agent prompts
  - Denial and escalation patterns
  - How you constrain tools and outputs consistently

---

### 4. The Silent Failure

- **Symptom:** A run “fails” — but logs are sparse, no traces exist, and no one knows what happened.
- **What it tests:**
  - Observability and trace design
  - Run state and audit trails
  - How you make agents debuggable in production

---

### 5. The Unevaluated Demo

- **Symptom:** The system looks great in demos, but there’s no systematic evaluation, no metrics, and no feedback loop.
- **What it tests:**
  - Evaluation harness design
  - Metrics and sampling strategy
  - How you close the loop from runs back to improvements

---

## Strategy

To defeat the Oracle Orchestrator Prime, the player must submit an **“Agentic Orchestrator Blueprint – Oracle Orchestrator Prime”** (markdown) that:

1. **Defines the agent graph and roles**
   - Which agents exist (planner, workers, critics, safety guard, tools router, etc.).
   - Clear responsibilities and hand-offs between them.
   - How state and context flow through the graph.

2. **Specifies tool contracts and error handling**
   - Concrete schemas or typed interfaces for tools.
   - Handling of timeouts, partial failures, and retries.
   - Guardrails around which agents may call which tools.

3. **Introduces a policy and guardrail layer**
   - System prompts or policies that enforce constraints.
   - How denials, redactions, and escalations are handled.
   - How to prevent agents from “escaping” safety constraints.

4. **Designs observability and resilience**
   - Which events are logged and how they are correlated per run.
   - How traces or timelines of decisions are captured.
   - Recovery strategies for stuck or partially-completed runs.

5. **Defines an evaluation and learning loop**
   - What metrics are tracked (task success, tool error rate, policy violations, etc.).
   - How runs are sampled and labeled.
   - How those signals feed back into prompts/policies/config.

---

## Boss Fight Shape

- **Submission Format:** markdown document titled

  > **“Agentic Orchestrator Blueprint – Oracle Orchestrator Prime”**

  Suggested sections:

  - `## Use Case & Requirements`
  - `## Agent Graph & Roles`
  - `## Tool Contracts & IO`
  - `## Policy & Guardrails`
  - `## Observability & Run State`
  - `## Evaluation & Improvement Loop`
  - `## Rollout & Risk Management`

- **Scenario:**

  You are asked to design a **multi-agent orchestration layer** for a realistic product (e.g., developer assistant, job search assistant, or data copilot). The orchestrator must:

  - coordinate multiple agents and tools,
  - respect safety and policy constraints,
  - be observable and debuggable,
  - and support ongoing improvement through evaluation.

The boss does not care which vendor or library you use. It cares whether the **design is coherent, safe, and operable**.

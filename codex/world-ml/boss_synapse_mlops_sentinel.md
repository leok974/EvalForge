# Boss Codex – ML Ops Sentinel

- **Boss ID:** `boss-synapse-mlops-sentinel`
- **World:** `world-ml` – The Synapse
- **Track:** `synapse-senior-mlops`
- **Stage:** 3 – Senior MLOps
- **Title:** ML Ops Sentinel
- **Tier:** Senior Boss

---

## Lore

Deep in the Synapse, beyond the training storms and gradient tempests, stands a quieter presence:

The **ML Ops Sentinel**.

It does not care how clever your model is.

It cares about:

- the half-finished notebooks that accidentally became production,
- the scripts that only one engineer can run,
- the model files that nobody knows how to roll back,
- the metrics that go red at 2am with no runbook in sight.

This boss tests whether you can turn **fragile, ad-hoc ML work** into a **platform and practice** that a whole team can operate safely.

---

## Attacks

### 1. Shadow Script Swarm

- **Symptom:** Dozens of training scripts, each with its own flags, paths, and magic environment variables.
- **What it tests:**  
  - Can you consolidate training into reproducible pipelines?  
  - Do you define standard entrypoints, configs, and artifact outputs?

---

### 2. Zombie Job Horde

- **Symptom:** Old scheduled jobs keep retraining and overwriting models with slightly different data or params. Nobody is sure which model is serving.
- **What it tests:**  
  - Job ownership and lifecycle  
  - Promotion workflows (staging → prod)  
  - Prevention of accidental “silent downgrades”

---

### 3. Drift Fog

- **Symptom:** Over months, model performance degrades. Alerts are noisy or non-existent. Some segments are clearly harmed, but nobody can point to a single dashboard.
- **What it tests:**  
  - Monitoring for data / target drift  
  - Segment-aware evaluation  
  - Clear, actionable alerting and triage

---

### 4. Governance Void

- **Symptom:** No model cards, no approvals, no paper trail when things change. Legal/compliance asks “who signed off on this?” and the room goes quiet.
- **What it tests:**  
  - Governance practices  
  - Documentation and approvals  
  - Auditability and risk management

---

## Strategy

To defeat the ML Ops Sentinel, the player must demonstrate a **platform-level plan**, not just a patchwork of tips:

1. **Lifecycle & Architecture**
   - Show how data, features, models, and deployments move through the system.
   - Make it clear which components are shared platform vs one-off project glue.

2. **CI/CD & Promotion**
   - Describe how models move from dev → training → evaluation → staging → prod.
   - Include gates (tests, metrics, canaries) and explicit promotion/rollback rules.

3. **Monitoring, Drift & Fairness**
   - Identify the metrics and dashboards required for safe operation.
   - Explain how you detect and respond to drift and regressions, especially for sensitive segments.

4. **Governance & Risk Controls**
   - Propose a light but real governance layer: model cards, approvals, and audit logs.
   - Keep it practical enough that engineers would actually follow it.

---

## Boss Fight Shape

- **Submission Format:** A markdown document titled  
  **“ML Platform Modernization Runbook – ML Ops Sentinel”**.

  Recommended sections:

  - `## Context & Current Pain`
  - `## Target Architecture – Data, Features, Models`
  - `## Training & CI/CD Pipeline`
  - `## Promotion, Canarying & Rollback`
  - `## Monitoring, Drift & Fairness`
  - `## Governance, Approvals & Auditability`
  - `## Phased Rollout Plan`

- **Scenario outline:**

  You join a team where:

  - Models are trained from personal notebooks.
  - There is no consistent pipeline, artifact store, or registry.
  - Deploys are done by copying files to servers or pasting weights into a UI.
  - Monitoring is ad-hoc; some dashboards exist but are incomplete.
  - There is growing concern about fairness and regulatory expectations.

  Your task is to design a **phased modernization plan** that:

  - introduces structure without freezing progress,
  - keeps risk manageable,
  - and creates a foundation for future models and teams.

The better your runbook balances **rigor, practicality, and risk-awareness**, the more HP you shave from the Sentinel.

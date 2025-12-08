# Boss Codex – Gradient Sentinel

- **Boss ID:** `boss-synapse-gradient-sentinel`
- **World:** `world-ml` – The Synapse
- **Track:** `synapse-tensor-gradient`
- **Stage:** `stage-1-synapse-tensor-gradient`
- **Title:** Gradient Sentinel
- **Tier:** Tensor & Gradient Boss (Stage 1 Capstone)

---

## Lore

At the center of the Synapse, gradients flicker like lightning across a neural storm.

Standing guard is the **Gradient Sentinel**.

It has watched engineers:

- celebrate a 99% accuracy on a broken train/val split,
- ship models with collapsed classes and silent data leaks,
- overfit tiny datasets with giant architectures,
- deploy without a clear baseline or monitoring.

To pass, you must prove you can **tame the learning loop**:

- choose appropriate metrics and splits,
- diagnose over/underfitting patterns,
- design experiments that actually answer questions,
- and write a runbook another ML engineer would trust on-call.

---

## Attacks

### 1. Mirage Accuracy

- **Symptom:** Training and validation accuracy are both very high, but real-world performance is poor.
- **In game:** The Sentinel shows suspiciously perfect curves and a weird label distribution.
- **What it tests:** Data leakage, bad splits, and unrealistic evaluation setups.

---

### 2. Gradient Collapse

- **Symptom:** Loss barely moves; gradients vanish or explode.
- **In game:** Curves show flat loss or NaNs after a few steps.
- **What it tests:** Learning rate, initialization, normalization, and debugging training stability.

---

### 3. Overfit Spiral

- **Symptom:** Training performance climbs, validation deteriorates.
- **In game:** The Sentinel reveals curves with widening train/val gaps.
- **What it tests:** Regularization, model capacity, augmentation, early stopping.

---

### 4. Drift Fog

- **Symptom:** A model that used to perform well slowly degrades in prod.
- **In game:** Distribution plots show feature drifts and label shifts over time.
- **What it tests:** Monitoring, recalibration, and retraining strategies.

---

## Strategy

To defeat the Gradient Sentinel, the player must demonstrate:

1. **Evaluation & Split Design**
   - Choose appropriate metrics for the task.
   - Design train/val/test (and possibly time-based) splits that avoid leakage.

2. **Training Loop Diagnostics**
   - Read loss/metric curves and logs.
   - Map typical pathologies (flat loss, divergence, overfitting) to concrete fixes.

3. **Experiment Design & Baselines**
   - Start from strong baselines.
   - Propose ablations and checkpoints that de-risk complexity.

4. **Production & Monitoring Awareness**
   - Think beyond local tests: drift, monitoring, and retraining.
   - Write procedures safe enough for a teammate to execute during an incident.

---

## Boss Fight Shape

- **Submission Format:** A markdown **“ML Training & Evaluation Incident Runbook”** with sections:

  - `## Incident Context`
  - `## Phase 1 – Verify Data & Splits`
  - `## Phase 2 – Inspect Metrics & Curves`
  - `## Phase 3 – Stabilize & Improve Training`
  - `## Phase 4 – Baseline & Experiments`
  - `## Phase 5 – Production Monitoring & Retraining`

- **Scenario (for the player):**

  You own a binary classification model that predicts **“risky vs safe”** for incoming requests.

  - Recently:
    - Offline metrics look excellent (AUC/accuracy).
    - In production, false negatives are high.
    - Retraining last month made things *worse*.
  - You suspect:
    - Data leakage in your validation split,
    - Mismatched distributions between offline data and prod,
    - And a brittle training loop with no proper baselines.

The runbook should:

- Audit the data and splits,
- Propose changes to the training loop and evaluation,
- Introduce baselines and simple ablations,
- And describe monitoring/retraining in a production context.

---
title: Metric
id: glossary/ml/metric
world: ml
level: beginner
tags: [evaluation, training, performance]
related:
  - codex:glossary/ml/loss
  - codex:glossary/ml/epoch
  - codex:glossary/world-ml/term-2
---

# Metric

## Definition
A **metric** is a measurement used to evaluate model performance (accuracy, F1, BLEU, ROC-AUC, etc.). Metrics may differ from the loss: you often optimize loss but report metrics that better match real success criteria.

## Usage
- Track progress during training.
- Choose models via validation metrics.
- Detect regression in production.

## Example
```py
# Conceptual accuracy
# accuracy = correct_predictions / total_predictions
```

## Pitfalls

* Optimizing for one metric can hurt another (precision vs recall tradeoff).
* Metrics can be misleading on imbalanced datasets without proper baselines.

## Related

* Loss: loss is optimized; metrics are reported.
* Epoch: metrics are tracked per epoch.
* Overfitting: watch metrics diverge between train/val (Term 2).

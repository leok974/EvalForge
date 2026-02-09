---
title: Loss
id: glossary/ml/loss
world: ml
level: beginner
tags: [training, optimization, metrics]
related:
  - codex:glossary/ml/metric
  - codex:glossary/ml/gradient
  - codex:glossary/world-ml/term-2
---

# Loss

## Definition
A **loss** is a scalar value that measures how wrong a model's predictions are compared to targets. Training minimizes loss; different tasks use different loss functions (MSE for regression, cross-entropy for classification).

## Usage
- Define the training objective.
- Compare training vs validation performance.
- Guide hyperparameter tuning.

## Example
```py
# Cross-entropy-like conceptual form:
# loss = -sum(y_true * log(y_pred))
```

## Pitfalls

* Lower training loss doesn't guarantee better generalization (watch validation).
* Loss scale differs by function; compare within the same loss type.

## Related

* Metric: metrics evaluate performance; loss is optimized.
* Gradient: gradients are computed from loss.
* Overfitting: training loss diverging from validation indicates overfitting (Term 2).

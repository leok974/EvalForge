---
title: Overfitting
id: glossary/world-ml/term-2
world: world-ml
level: intermediate
tags: [training, generalization, debugging]
related:
  - codex:glossary/world-ml/term-3
  - codex:glossary/ml/metric
  - codex:glossary/ml/loss
---

# Overfitting

## Definition
**Overfitting** happens when a model learns patterns specific to the training data (including noise) and performs worse on new data. It often appears as training performance improving while validation performance stalls or degrades.

## Usage
- Diagnose with train vs validation curves.
- Decide when to stop training (early stopping).
- Trigger regularization or data augmentation.

## Example
```py
# Symptom pattern (conceptual):
# train_loss ↓ steadily
# val_loss   ↓ then ↑

# Detection:
if val_loss > best_val_loss:
    patience_counter += 1
    if patience_counter > early_stop_patience:
        print("Early stopping triggered")
        break
```

## Pitfalls

* Overfitting can look like "great training accuracy" but poor real-world results.
* Leakage (using future info or target-like features) can mimic overfitting.

## Related

* Regularization: regularization prevents overfitting (Term 3).
* Metric: watch metrics diverge between train/val.
* Loss: training loss diverging from validation indicates overfitting.

---
title: Regularization
id: glossary/world-ml/term-3
world: world-ml
level: intermediate
tags: [training, generalization, techniques]
related:
  - codex:glossary/world-ml/term-2
  - codex:glossary/ml/loss
  - codex:glossary/ml/learning-rate
---

# Regularization

## Definition
**Regularization** is any technique that reduces overfitting by discouraging overly complex models. Common methods include weight decay (L2), dropout, data augmentation, and early stopping.

## Usage
- Improve generalization.
- Stabilize training.
- Prevent weights from growing too large.

## Example
```py
# L2 / weight decay conceptual:
# loss_total = loss_data + lambda * sum(w^2)

# In PyTorch:
optimizer = torch.optim.Adam(model.parameters(), 
                             lr=0.001, 
                             weight_decay=1e-4)  # L2 regularization
```

## Pitfalls

* Too much regularization causes underfitting (model can't learn the signal).
* Regularization strength often interacts with learning rate and batch size.

## Related

* Overfitting: regularization prevents overfitting (Term 2).
* Loss: regularization adds a penalty term to the loss.
* Learning Rate: regularization strength interacts with learning rate.

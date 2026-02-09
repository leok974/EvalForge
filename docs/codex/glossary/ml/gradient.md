---
title: Gradient
id: glossary/ml/gradient
world: ml
level: intermediate
tags: [optimization, training, backpropagation]
related:
  - codex:glossary/ml/loss
  - codex:glossary/ml/learning-rate
  - codex:glossary/ml/epoch
---

# Gradient

## Definition
A **gradient** measures how a function changes as its inputs change—formally, the partial derivatives of a loss with respect to parameters. Training via gradient descent updates parameters in the direction that reduces loss.

## Usage
- Compute parameter updates during backpropagation.
- Diagnose training (vanishing/exploding gradients).
- Tune learning rate and normalization strategies.

## Example
```py
# Conceptual pseudo-code (framework-agnostic)
loss = compute_loss(preds, targets)
grads = dloss_dparams(loss, params)
params = params - lr * grads
```

## Pitfalls

* Gradients can vanish (too small) or explode (too large), breaking training.
* Gradients depend on the current batch—noise is normal.

## Related

* Loss: gradients measure how loss changes with parameters.
* Learning Rate: learning rate scales gradient updates.
* Epoch: gradients are computed many times per epoch.

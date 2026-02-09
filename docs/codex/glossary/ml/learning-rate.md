---
title: Learning Rate
id: glossary/ml/learning-rate
world: ml
level: intermediate
tags: [optimization, training, hyperparameters]
related:
  - codex:glossary/ml/gradient
  - codex:glossary/ml/loss
  - codex:glossary/ml/epoch
---

# Learning Rate

## Definition
The **learning rate** controls the step size of parameter updates during optimization. Too high can cause divergence; too low can make training painfully slow or get stuck.

## Usage
- Tune convergence speed vs stability.
- Use schedules (warmup, decay) to improve training.
- Different LRs for different parameter groups (advanced).

## Example
```py
# Conceptual update rule
params = params - lr * gradient
```

## Pitfalls

* High LR may look "good" early then suddenly explode.
* Changing LR often changes optimal batch size and regularization needs.

## Related

* Gradient: learning rate scales gradient updates.
* Loss: learning rate affects how quickly loss decreases.
* Epoch: learning rate often decays over epochs.

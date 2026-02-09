---
title: Batch
id: glossary/world-ml/term-1
world: world-ml
level: beginner
tags: [training, optimization, data-loading]
related:
  - codex:glossary/ml/epoch
  - codex:glossary/ml/learning-rate
  - codex:glossary/ml/gradient
---

# Batch

## Definition
A **batch** is a subset of training examples processed together in one forward/backward pass. Batch size affects speed, memory usage, and the "noise" in gradient estimates.

## Usage
- Train with mini-batch gradient descent.
- Tune batch size for GPU/CPU memory limits.
- Improve stability with larger batches (sometimes).

## Example
```py
# batch: shape (batch_size, features)
# e.g., images: (batch_size, channels, height, width)

for batch in dataloader:
    predictions = model(batch['inputs'])
    loss = loss_fn(predictions, batch['targets'])
    loss.backward()
    optimizer.step()
```

## Pitfalls

* Very small batches can make training unstable; very large batches can generalize worse without LR tuning.
* Batch size changes often require learning-rate adjustment.

## Related

* Epoch: an epoch consists of many batches.
* Learning Rate: batch size affects optimal learning rate.
* Gradient: batch size affects gradient noise.

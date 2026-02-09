---
title: Epoch
id: glossary/ml/epoch
world: ml
level: beginner
tags: [training, optimization, iteration]
related:
  - codex:glossary/world-ml/term-1
  - codex:glossary/ml/learning-rate
  - codex:glossary/world-ml/term-2
---

# Epoch

## Definition
An **epoch** is one full pass over the training dataset. Training typically runs for multiple epochs, updating parameters many times using mini-batches.

## Usage
- Organize training loops.
- Schedule learning-rate decay per epoch.
- Monitor overfitting as epochs increase.

## Example
```py
for epoch in range(num_epochs):
  for batch in dataloader:
    train_step(batch)
```

## Pitfalls

* More epochs can improve training loss while worsening validation (overfitting).
* If your dataset is huge or streaming, "epoch" can be a fuzzy concept.

## Related

* Batch: an epoch consists of many batches (Term 1).
* Learning Rate: learning rate often decays per epoch.
* Overfitting: too many epochs can cause overfitting (Term 2).

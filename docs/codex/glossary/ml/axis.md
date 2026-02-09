---
title: Axis
id: glossary/ml/axis
world: ml
level: beginner
tags: [tensors, linear-algebra, operations]
related:
  - codex:glossary/ml/shape
  - codex:glossary/ml/tensor
  - codex:glossary/ml/reshape
---

# Axis

## Definition
An **axis** is a numbered dimension of a tensor. In most ML libraries, `axis=0` refers to the first dimension, `axis=1` the second, and so on. Many operations (sum, mean, argmax) require an axis to define *which dimension to reduce or operate across*.

## Usage
- Reduce across features vs across batch.
- Pick class dimension for `argmax`.
- Normalize along a specific dimension.

## Example
```py
import numpy as np

x = np.array([[1, 2, 3],
              [4, 5, 6]])

col_sum = x.sum(axis=0)  # [5, 7, 9]
row_sum = x.sum(axis=1)  # [6, 15]
```

## Pitfalls

* Axis meaning depends on your shape convention (e.g., `[batch, features]` vs `[features, batch]`).
* Negative axes (e.g., `axis=-1`) are common and can be clearer than counting.

## Related

* Shape: shape defines how many axes a tensor has.
* Tensor: tensors have multiple axes.
* Reshape: reshaping changes axis structure.

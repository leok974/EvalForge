---
title: Tensor
id: glossary/ml/tensor
world: ml
level: beginner
tags: [data-structures, linear-algebra, fundamentals]
related:
  - codex:glossary/ml/shape
  - codex:glossary/ml/reshape
  - codex:glossary/ml/broadcasting
---

# Tensor

## Definition
A **tensor** is a multi-dimensional array used to represent data in ML (scalars, vectors, matrices, and higher-order arrays). Tensors store both values and shape, and ML operations are defined in terms of tensor math.

## Usage
- Represent input data (images, text embeddings).
- Store weights/activations.
- Perform vectorized operations efficiently.

## Example
```py
import numpy as np

scalar = np.array(3.14)          # shape ()
vector = np.array([1, 2, 3])     # shape (3,)
matrix = np.array([[1, 2], [3, 4]])  # shape (2, 2)
```

## Pitfalls

* "Tensor" can mean different concrete types (NumPy ndarray, PyTorch Tensor), but the concepts carry over.
* Shape mismatches often surface far from the root cause—print shapes early.

## Related

* Shape: every tensor has a shape.
* Reshape: reshape changes tensor shape.
* Broadcasting: broadcasting enables operations between different-shaped tensors.

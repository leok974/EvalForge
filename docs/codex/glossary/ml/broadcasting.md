---
title: Broadcasting
id: glossary/ml/broadcasting
world: ml
level: intermediate
tags: [tensors, operations, linear-algebra]
related:
  - codex:glossary/ml/shape
  - codex:glossary/ml/axis
  - codex:glossary/ml/tensor
---

# Broadcasting

## Definition
**Broadcasting** is a rule that allows operations between tensors of different shapes by automatically expanding dimensions of size 1. This enables vectorized math like subtracting a `(features,)` vector from a `(batch, features)` matrix.

## Usage
- Add bias to a batch of activations.
- Normalize features by subtracting mean.
- Scale tensors without explicit loops.

## Example
```py
import numpy as np

x = np.array([[1., 2., 3.],
              [4., 5., 6.]])     # (2, 3)
b = np.array([10., 20., 30.])    # (3,)
y = x + b                        # (2, 3) broadcast b across rows
```

## Pitfalls

* Broadcasting can hide shape bugs; confirm shapes before/after operations.
* Unintended broadcasting can silently produce wrong results.

## Related

* Shape: broadcasting depends on compatible shapes.
* Axis: broadcasting expands along specific axes.
* Tensor: broadcasting operates on tensors.

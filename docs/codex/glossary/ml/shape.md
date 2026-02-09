---
title: Shape
id: glossary/ml/shape
world: ml
level: beginner
tags: [tensors, linear-algebra, debugging]
related:
  - codex:glossary/ml/axis
  - codex:glossary/ml/tensor
  - codex:glossary/ml/reshape
---

# Shape

## Definition
A tensor's **shape** is the size of each dimension (e.g., `(batch, channels, height, width)`). Shape tells you how data is laid out in memory and how operations like matrix multiplication, convolution, and broadcasting will behave.

## Usage
- Verify model inputs/outputs.
- Debug dimension mismatch errors.
- Decide which axis to reduce or normalize.

## Example
```py
import numpy as np
x = np.zeros((32, 128))   # batch=32, features=128
print(x.shape)            # (32, 128)
```

## Pitfalls

* Mixing up batch vs feature dimensions is a top source of bugs.
* Some libs show shapes as lists, others as tuples; the meaning is the same.

## Related

* Axis: axis refers to dimensions within a shape.
* Tensor: all tensors have a shape.
* Reshape: reshape changes the shape while preserving data.

---
title: Reshape
id: glossary/ml/reshape
world: ml
level: beginner
tags: [tensors, operations, data-manipulation]
related:
  - codex:glossary/ml/shape
  - codex:glossary/ml/axis
  - codex:glossary/ml/broadcasting
---

# Reshape

## Definition
**Reshape** changes a tensor's shape without changing its underlying data (when possible). It's used to prepare data for layers (e.g., flatten before dense layers) or to align dimensions for operations.

## Usage
- Flatten `(batch, channels, height, width)` → `(batch, features)`.
- Add/remove singleton dims for broadcasting.
- Convert between compatible views of the same data.

## Example
```py
import numpy as np

x = np.zeros((32, 3, 64, 64))
flat = x.reshape(32, -1)  # (32, 12288)
```

## Pitfalls

* Reshape requires the total number of elements to match.
* Some frameworks need contiguous memory for view/reshape; non-contiguous tensors may require a copy.

## Related

* Shape: reshape changes the shape.
* Axis: reshaping changes axis structure.
* Broadcasting: reshaping is often used to enable broadcasting.

## Outcome
You will learn how to reason about array (tensor) shapes in NumPy so operations like reshape, indexing, and matrix multiplication work predictably.

## Concept in 30 seconds
A “tensor” here is just an N-dimensional array. The most important idea is **shape**: a tuple describing dimensions. Operations succeed or fail based on shape rules. If you can answer “what is the shape before and after this operation?” you can debug most tensor issues quickly.

## Key terms
- **Tensor / Array**: An N-dimensional grid of numbers.
- **Shape**: The size of each dimension (e.g., (3, 2)).
- **Axis**: Which dimension an operation applies to.
- **Broadcasting**: Expanding smaller shapes to match larger ones by rules.
- **Reshape**: Reinterpreting data with a new shape (same total size).

## Walkthrough
1) Print shapes early and often (`arr.shape`).
2) Use reshape when you need a specific dimensional structure.
3) For matrix multiplication, confirm inner dimensions match.
4) For reductions (sum/mean), specify the axis you intend.
5) Click **Run** to verify shapes at each step.
6) Use **Submit** when your operations produce outputs with the expected shapes.

## Example implementation
Shape basics with a few common operations:

```py
import numpy as np

a = np.array([1, 2, 3, 4, 5, 6])
print("a.shape:", a.shape)  # (6,)

m = a.reshape(2, 3)
print("m.shape:", m.shape)  # (2, 3)

# Sum across axis 0 (down columns) vs axis 1 (across rows)
print("sum axis=0:", m.sum(axis=0), "shape:", m.sum(axis=0).shape)  # (3,)
print("sum axis=1:", m.sum(axis=1), "shape:", m.sum(axis=1).shape)  # (2,)

# Matrix multiply: (2,3) @ (3,2) -> (2,2)
w = np.ones((3, 2))
out = m @ w
print("out.shape:", out.shape)  # (2,2)

# Broadcasting: (2,3) + (3,) -> (2,3)
b = np.array([10, 20, 30])
print((m + b).shape)
```

## Common mistakes
- **Reshaping to an incompatible size** (total elements must match).
- **Using `*` when you meant matrix multiply (`@`)**.
- **Summing the wrong axis** (shape changes differently by axis).
- **Broadcasting surprises** (verify the smaller shape aligns from the right).
- **Losing a dimension accidentally** (e.g., slicing a row vs keeping it 2D).

## Check yourself
- What does shape (2, 3) mean?
- Why does (2,3) @ (3,2) work but (2,3) @ (2,3) fails?
- When you sum over axis=1, which dimension disappears?

# Axis

## Definition
An **axis** is a dimension index along which an operation is applied. In a 2D array with shape `(rows, cols)`, axis 0 refers to rows (down columns), and axis 1 refers to columns (across rows).

## Tiny example
For `m.shape == (2, 3)`:
- `m.sum(axis=0)` returns shape `(3,)`
- `m.sum(axis=1)` returns shape `(2,)`

## Common pitfall
Summing or averaging the wrong axis produces the wrong shape and can silently break later computations. Always check shapes after reductions.

## Related
Shape, Broadcasting

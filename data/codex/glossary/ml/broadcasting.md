# Broadcasting

## Definition
**Broadcasting** is a set of rules that allows elementwise operations on arrays with different shapes by expanding dimensions (without copying data) when compatible.

## Tiny example
Adding `(2, 3) + (3,)` works because the `(3,)` aligns to the last dimension and expands across the first dimension.

## Common pitfall
Broadcasting aligns dimensions from the right. If shapes don’t align, you’ll get errors or unexpected results. When confused, reshape explicitly to make dimensions match.

## Related
Shape, Axis

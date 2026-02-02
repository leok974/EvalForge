# Shape

## Definition
**Shape** is a tuple describing the size of each dimension of an array. For example, shape `(2, 3)` means 2 rows and 3 columns.

## Tiny example
If `a.shape == (6,)`, then `a.reshape(2, 3)` becomes shape `(2, 3)` because 2×3 = 6.

## Common pitfall
Reshape can only work if the total number of elements stays the same. If the product of the new shape doesn’t match the original size, you’ll get an error.

## Related
Reshape, Broadcasting

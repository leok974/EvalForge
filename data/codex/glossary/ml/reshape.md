# Reshape

## Definition
**Reshape** changes the shape of an array without changing its underlying data size. It’s used to organize data into the dimensions required by an operation.

## Tiny example
`np.array([1,2,3,4]).reshape(2,2)` becomes a 2×2 matrix.

## Common pitfall
Reshape is not “free” if the data layout isn’t compatible; some reshapes may require copying. For starter tasks, the big rule is: total element count must remain the same.

## Related
Shape, Tensor / Array

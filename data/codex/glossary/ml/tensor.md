# Tensor / Array

## Definition
A **tensor** is an N-dimensional array of numbers. In this course, you can think of it as a NumPy array. Tensors store data (inputs, weights, outputs) in machine learning.

## Tiny example
A vector is a 1D tensor: shape `(3,)`.
A matrix is a 2D tensor: shape `(2, 3)`.

## Common pitfall
Most bugs come from shape mismatches. If an operation fails, print shapes before and after each step. Shape reasoning is the fastest way to debug ML code.

## Related
Shape, Axis

# Loss

## Definition
**Loss** is a number that measures how wrong a model’s predictions are. Training aims to reduce loss over time. Different tasks use different loss functions (MSE for regression, cross-entropy for classification).

## Tiny example
If the true value is 10 and the prediction is 7, a simple squared loss is `(7 - 10)^2 = 9`.

## Common pitfall
A decreasing loss doesn’t guarantee the model generalizes well. You also need validation metrics to detect overfitting. But for a starter loop, loss decreasing is the first sign learning is happening.

## Related
Gradient, Metric

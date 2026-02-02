# Gradient

## Definition
A **gradient** tells you how to change model parameters to reduce loss. It’s the slope of the loss function with respect to weights. Gradient descent updates weights in the *negative* gradient direction.

## Tiny example
If increasing a weight increases loss, the gradient is positive, so you subtract a positive number to move the weight down.

## Common pitfall
Updating in the wrong direction (`+=` instead of `-=`) makes loss increase. Another common issue is forgetting to average gradients, causing huge steps as dataset size grows.

## Related
Loss, Learning Rate

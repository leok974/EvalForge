# Learning Rate

## Definition
The **learning rate** controls how large each update step is during training. It scales the gradient update. Too large can cause divergence; too small can make training painfully slow.

## Tiny example
Update rule:
`w = w - lr * grad`
If `lr` is 0.1, you step 10× larger than `lr` 0.01.

## Common pitfall
When loss explodes, reduce the learning rate. When loss barely changes, increase it slightly or train longer. The learning rate is often the first knob to adjust.

## Related
Gradient, Epoch

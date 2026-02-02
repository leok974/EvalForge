# Epoch

## Definition
An **epoch** is one full pass through the training dataset. Many training loops iterate over multiple epochs so the model can gradually improve.

## Tiny example
If you have 1,000 training examples and you process all 1,000 once, that’s one epoch.

## Common pitfall
More epochs is not always better: you can overfit (training loss goes down while validation loss goes up). For starters, it’s enough to confirm the loss trend is moving in the right direction.

## Related
Metric, Loss

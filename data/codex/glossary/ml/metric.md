# Metric

## Definition
A **metric** is a tracked value used to evaluate training progress. Loss is a metric, but you may also track accuracy, precision, recall, or mean absolute error depending on the task.

## Tiny example
Printing `loss` every 10 epochs shows whether training is improving.

## Common pitfall
Comparing metrics across different scales without context can mislead you. Always define what “good” looks like for your task, and track metrics consistently (same data split, same units).

## Related
Loss, Epoch

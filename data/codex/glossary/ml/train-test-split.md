---
title: Train-Test Split
id: ml/train-test-split
---
# Train-Test Split

Divides data into training and testing sets.

## Purpose
- **Train**: Learn patterns
- **Test**: Evaluate generalization

## Example
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

## Typical Ratio
80% train, 20% test

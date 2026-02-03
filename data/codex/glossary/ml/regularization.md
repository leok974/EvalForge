---
title: Regularization
id: ml/regularization
---
# Regularization

Techniques to prevent overfitting.

## Common Methods
- **L1 (Lasso)**: Adds absolute value of weights
- **L2 (Ridge)**: Adds squared weights
- **Dropout**: Randomly disable neurons (neural nets)
- **Early Stopping**: Stop training before overfitting

## Scikit-learn Example
```python
from sklearn.linear_model import Ridge
model = Ridge(alpha=1.0)  # alpha = regularization strength
```

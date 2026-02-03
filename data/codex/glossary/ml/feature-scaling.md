---
title: Feature Scaling
id: ml/feature-scaling
---
# Feature Scaling

Transforms features to similar ranges.

## Methods
- **Normalization**: Scale to [0, 1]
  ```python
  from sklearn.preprocessing import MinMaxScaler
  ```
- **Standardization**: Mean=0, StdDev=1
  ```python
  from sklearn.preprocessing import StandardScaler
  ```

## When Needed
- Distance-based algorithms (KNN, SVM)
- Gradient descent optimization

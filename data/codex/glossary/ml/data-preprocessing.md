---
title: Data Preprocessing
id: ml/data-preprocessing
---
# Data Preprocessing

Preparing raw data for machine learning.

## Common Steps
1. **Handle Missing Values**: Imputation or removal
2. **Scaling**: Normalize or standardize features
3. **Encoding**: Convert categorical to numerical
4. **Feature Engineering**: Create new features

## Example
```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

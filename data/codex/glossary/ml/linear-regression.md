---
title: Linear Regression
id: ml/linear-regression
---
# Linear Regression

Predicts continuous values using a linear relationship.

## Formula
```
y = mx + b
```

## Scikit-learn Example
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

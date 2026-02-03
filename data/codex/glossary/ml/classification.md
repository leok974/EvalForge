---
title: Classification
id: ml/classification
---
# Classification

Predicts categorical labels (classes).

## Common Algorithms
- Logistic Regression
- Decision Trees
- Random Forest
- SVM

## Example
```python
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression()
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
```

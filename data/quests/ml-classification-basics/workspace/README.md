# Classification Basics — kNN (Deterministic)

Implement a tiny k-Nearest Neighbors classifier:

- `fit_knn(X_train, y_train, k)` returns a model dict
- `predict_knn(model, X)` returns predicted labels (0/1) using:
  - Euclidean distance
  - Majority vote
  - Ties break toward label 0 (deterministic)

All inputs are numpy arrays.

import numpy as np
from typing import Dict, Any

def fit_knn(X_train: np.ndarray, y_train: np.ndarray, k: int) -> Dict[str, Any]:
    return {
        "X_train": np.asarray(X_train, dtype=float),
        "y_train": np.asarray(y_train, dtype=int),
        "k": int(k),
    }

def predict_knn(model: Dict[str, Any], X: np.ndarray) -> np.ndarray:
    X_train = model["X_train"]
    y_train = model["y_train"]
    k = int(model["k"])

    X = np.asarray(X, dtype=float)
    preds = []
    for x in X:
        d2 = np.sum((X_train - x) ** 2, axis=1)
        idx = np.argsort(d2)[:k]
        votes = y_train[idx]
        ones = int(np.sum(votes == 1))
        zeros = k - ones
        preds.append(1 if ones > zeros else 0)  # tie -> 0
    return np.array(preds, dtype=int)

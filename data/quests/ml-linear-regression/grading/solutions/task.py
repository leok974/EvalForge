import numpy as np
from typing import Tuple

def fit_linear_regression(X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, float]:
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)

    # Add bias column
    Xb = np.concatenate([np.ones((X.shape[0], 1)), X], axis=1)
    w = np.linalg.pinv(Xb) @ y  # (d+1,)
    intercept = float(w[0])
    coef = w[1:]
    return coef, intercept

def predict_linear(X: np.ndarray, coef: np.ndarray, intercept: float) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    coef = np.asarray(coef, dtype=float)
    return X @ coef + float(intercept)

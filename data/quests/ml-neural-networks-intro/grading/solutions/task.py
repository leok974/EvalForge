import numpy as np

def dense_forward(X: np.ndarray, W: np.ndarray, b: np.ndarray, activation: str) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    W = np.asarray(W, dtype=float)
    b = np.asarray(b, dtype=float)

    Z = X @ W + b
    if activation == "relu":
        return np.maximum(0.0, Z)
    if activation == "sigmoid":
        return 1.0 / (1.0 + np.exp(-Z))
    raise ValueError("activation must be 'relu' or 'sigmoid'")

import numpy as np

def dense_forward(X, W, b, activation="relu"):
    Z = X @ W + b
    if activation == "relu":
        return np.maximum(0, Z)
    elif activation == "sigmoid":
        return 1 / (1 + np.exp(-Z))
    return Z
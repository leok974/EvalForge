import numpy as np

def ridge_loss(y_true: np.ndarray, y_pred: np.ndarray, coef: np.ndarray, alpha: float) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    coef = np.asarray(coef, dtype=float)

    mse = float(np.mean((y_true - y_pred) ** 2))
    penalty = float(alpha) * float(np.sum(coef ** 2))
    return mse + penalty

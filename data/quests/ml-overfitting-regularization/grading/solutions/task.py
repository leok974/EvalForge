import numpy as np

def ridge_loss(y_true, y_pred, coef, alpha):
    mse = np.mean((y_true - y_pred)**2)
    penalty = alpha * np.sum(coef**2)
    return mse + penalty
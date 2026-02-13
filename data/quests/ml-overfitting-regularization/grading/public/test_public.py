import numpy as np
from task import ridge_loss

def test_ridge_loss_value():
    y_true = np.array([1.0, 2.0, 3.0])
    y_pred = np.array([1.0, 2.5, 2.0])
    coef = np.array([2.0, -1.0])
    alpha = 0.1

    mse = ((0.0**2) + (0.5**2) + ((-1.0)**2)) / 3.0  # (0 + 0.25 + 1)/3 = 0.416666...
    penalty = 0.1 * (4 + 1)  # 0.5
    expected = mse + penalty

    out = ridge_loss(y_true, y_pred, coef, alpha)
    assert abs(out - expected) < 1e-12

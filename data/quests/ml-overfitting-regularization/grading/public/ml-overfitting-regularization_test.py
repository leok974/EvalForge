import pytest
import numpy as np
from workspace.task import ridge_loss

def test_ridge():
    y_true = np.array([1, 2])
    y_pred = np.array([1, 2]) # MSE = 0
    coef = np.array([1, -1])  # sum sq = 2
    alpha = 0.5
    
    # Loss = 0 + 0.5 * 2 = 1.0
    loss = ridge_loss(y_true, y_pred, coef, alpha)
    assert loss == 1.0
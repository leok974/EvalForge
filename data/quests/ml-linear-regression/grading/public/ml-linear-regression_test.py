import pytest
import numpy as np
from workspace.task import fit_predict

def test_linear_regression():
    # Simple y = 2x
    X = np.array([[1], [2], [3]])
    y = np.array([2, 4, 6])
    coef, intercept, preds = fit_predict(X, y)
    
    np.testing.assert_allclose(coef, [2.0], atol=1e-5)
    np.testing.assert_allclose(intercept, 0.0, atol=1e-5)
    np.testing.assert_allclose(preds, y, atol=1e-5)
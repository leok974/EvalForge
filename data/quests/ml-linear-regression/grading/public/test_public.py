import numpy as np
from task import fit_linear_regression, predict_linear

def test_fit_predict_line():
    # y = 2*x + 1 exactly
    X = np.array([[0.0], [1.0], [2.0], [3.0]])
    y = np.array([1.0, 3.0, 5.0, 7.0])

    coef, intercept = fit_linear_regression(X, y)
    assert coef.shape == (1,)
    assert abs(intercept - 1.0) < 1e-9
    assert abs(coef[0] - 2.0) < 1e-9

    preds = predict_linear(np.array([[4.0], [5.0]]), coef, intercept)
    assert np.allclose(preds, np.array([9.0, 11.0]))

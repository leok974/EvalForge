import pytest
import numpy as np
from workspace.task import knn_predict

def test_knn():
    X_train = np.array([[0], [1], [2], [10], [11], [12]])
    y_train = np.array([0, 0, 0, 1, 1, 1])
    
    X_test = np.array([[0.5], [11.5]])
    
    preds = knn_predict(X_train, y_train, X_test, k=3)
    np.testing.assert_array_equal(preds, [0, 1])
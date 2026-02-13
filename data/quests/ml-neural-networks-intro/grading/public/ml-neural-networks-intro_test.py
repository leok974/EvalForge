import pytest
import numpy as np
from workspace.task import dense_forward

def test_dense_relu():
    X = np.array([[1, -1]])
    W = np.array([[1, 1], [0, 1]]) # (2,2)
    b = np.array([0, 1])
    # Z = X@W + b = [1, 0] + [0, 1] = [1, 1]
    # Relu([1, 1]) = [1, 1]
    
    out = dense_forward(X, W, b, activation="relu")
    np.testing.assert_array_equal(out, [[1, 1]])

def test_dense_sigmoid():
    X = np.array([[0, 0]])
    W = np.zeros((2,1))
    b = np.array([0])
    # Z = 0
    # Sigmoid(0) = 0.5
    out = dense_forward(X, W, b, activation="sigmoid")
    np.testing.assert_allclose(out, [[0.5]], atol=1e-5)
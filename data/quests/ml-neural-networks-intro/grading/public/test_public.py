import numpy as np
from task import dense_forward

def test_dense_relu():
    X = np.array([[1, 2]], dtype=float)         # (1,2)
    W = np.array([[1, -1], [2, 0]], dtype=float) # (2,2)
    b = np.array([0.5, -0.5], dtype=float)      # (2,)

    out = dense_forward(X, W, b, "relu")
    # Z = [1*1+2*2+0.5, 1*-1+2*0-0.5] = [5.5, -1.5] -> relu => [5.5, 0]
    assert np.allclose(out, np.array([[5.5, 0.0]]))

def test_dense_sigmoid_shape():
    X = np.array([[0, 0],[1,1]], dtype=float)
    W = np.ones((2,3), dtype=float)
    b = np.zeros((3,), dtype=float)
    out = dense_forward(X, W, b, "sigmoid")
    assert out.shape == (2,3)
    assert np.all((out >= 0.0) & (out <= 1.0))

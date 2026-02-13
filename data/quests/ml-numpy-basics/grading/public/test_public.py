import numpy as np
from task import normalize_minmax

def test_normalize_basic():
    x = np.array([2, 4, 6], dtype=float)
    out = normalize_minmax(x)
    assert np.allclose(out, np.array([0.0, 0.5, 1.0]))
    assert np.allclose(x, np.array([2, 4, 6], dtype=float))  # no mutation

def test_normalize_constant():
    x = np.array([3, 3, 3], dtype=float)
    out = normalize_minmax(x)
    assert np.allclose(out, np.array([0.0, 0.0, 0.0]))

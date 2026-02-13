import pytest
import numpy as np
from workspace.task import normalize

def test_normalize_simple():
    arr = np.array([10, 20, 30])
    res = normalize(arr)
    expected = np.array([0.0, 0.5, 1.0])
    np.testing.assert_allclose(res, expected, atol=1e-5)

def test_normalize_constant():
    arr = np.array([5, 5, 5])
    res = normalize(arr)
    expected = np.zeros(3)
    np.testing.assert_allclose(res, expected, atol=1e-5)
import pytest
import numpy as np
from workspace.task import split_data

def test_split_deterministic():
    X = np.arange(100).reshape(100, 1)
    y = np.arange(100)
    
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, seed=42)
    
    # Check sizes
    assert len(X_test) == 20
    assert len(X_train) == 80
    
    # Check determinism (repeating gives same result)
    X_tr2, X_te2, y_tr2, y_te2 = split_data(X, y, test_size=0.2, seed=42)
    np.testing.assert_array_equal(X_test, X_te2)
    np.testing.assert_array_equal(y_test, y_te2)
    
    # Check shuffle happened (highly likely)
    assert not np.array_equal(y_train, np.arange(80))
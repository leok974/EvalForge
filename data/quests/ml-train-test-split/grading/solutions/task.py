import numpy as np
import math

def split_data(X, y, test_size=0.2, seed=42):
    rng = np.random.default_rng(seed)
    n = len(X)
    n_test = math.ceil(n * test_size)
    
    indices = np.arange(n)
    rng.shuffle(indices)
    
    test_idx = indices[-n_test:]
    train_idx = indices[:-n_test]
    
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]
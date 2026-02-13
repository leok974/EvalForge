import numpy as np
import math
from typing import Tuple

def train_test_split(
    X: np.ndarray,
    y: np.ndarray,
    test_size: float,
    seed: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    X = np.asarray(X)
    y = np.asarray(y)
    n = X.shape[0]

    rs = np.random.RandomState(seed)
    idx = rs.permutation(n)

    n_test = int(math.ceil(n * float(test_size)))
    test_idx = idx[-n_test:]
    train_idx = idx[:-n_test]

    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]

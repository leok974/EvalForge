import numpy as np
from task import train_test_split

def test_split_deterministic_and_aligned():
    X = np.arange(20).reshape(10, 2)
    y = np.arange(10)

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, seed=123)

    assert Xtr.shape == (7, 2)
    assert Xte.shape == (3, 2)
    assert ytr.shape == (7,)
    assert yte.shape == (3,)

    # alignment: first column /2 should equal label *2? Actually X rows are [2k,2k+1], so label k
    assert np.all((Xtr[:, 0] // 2) == ytr)
    assert np.all((Xte[:, 0] // 2) == yte)

    # determinism
    Xtr2, Xte2, ytr2, yte2 = train_test_split(X, y, test_size=0.3, seed=123)
    assert np.array_equal(Xtr, Xtr2)
    assert np.array_equal(Xte, Xte2)
    assert np.array_equal(ytr, ytr2)
    assert np.array_equal(yte, yte2)

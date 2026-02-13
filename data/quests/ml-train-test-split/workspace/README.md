# Train/Test Split — Deterministic

Implement `train_test_split(X, y, test_size, seed)`:

- X: numpy array shape (n, d)
- y: numpy array shape (n,)
- test_size: float in (0, 1)
- seed: int
- Shuffle indices using the seed, then take the last `ceil(n * test_size)` as test
- Return: (X_train, X_test, y_train, y_test)

import numpy as np

def knn_predict(X_train, y_train, X_test, k=3):
    preds = []
    for x in X_test:
        # Distances
        dists = np.sqrt(np.sum((X_train - x)**2, axis=1))
        # Nearest k indices
        idx = np.argsort(dists)[:k]
        # Vote
        labels = y_train[idx]
        counts = np.bincount(labels, minlength=2)
        # Tie break to 0 is implicit if counts equal and argmax picks first
        # But for strict determinism we can just use argmax which works
        preds.append(np.argmax(counts))
    return np.array(preds)
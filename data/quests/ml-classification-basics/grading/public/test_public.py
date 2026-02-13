import numpy as np
from task import fit_knn, predict_knn

def test_knn_predicts_expected():
    X_train = np.array([[0,0],[0,1],[1,0],[1,1],[10,10],[10,11],[11,10],[11,11]], dtype=float)
    y_train = np.array([0,0,0,0, 1,1,1,1], dtype=int)

    model = fit_knn(X_train, y_train, k=3)
    X = np.array([[0.2,0.2], [10.2,10.2], [5,5]], dtype=float)

    pred = predict_knn(model, X)
    assert pred.tolist() == [0, 1, 0]  # middle is ambiguous but closer to cluster 0 with k=3 + tie rule

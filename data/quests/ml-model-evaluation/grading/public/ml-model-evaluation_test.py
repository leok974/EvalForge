import pytest
import numpy as np
from workspace.task import evaluate

def test_metrics():
    y_true = np.array([0, 1, 1, 1])
    y_pred = np.array([0, 0, 1, 1])
    # TP=2, FP=0, FN=1, TN=1
    # Acc = 3/4 = 0.75
    # Prec = 2/2 = 1.0
    # Rec = 2/3 = 0.666...
    # F1 = 2*1*0.66/(1+0.66) = 0.8
    
    metrics = evaluate(y_true, y_pred)
    
    assert metrics["accuracy"] == 0.75
    assert metrics["precision"] == 1.0
    assert abs(metrics["recall"] - 2/3) < 1e-5
    assert abs(metrics["f1"] - 0.8) < 1e-5
    np.testing.assert_array_equal(metrics["confusion_matrix"], [[1, 0], [1, 2]])
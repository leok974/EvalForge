from task import evaluate_binary

def test_metrics_and_confusion():
    y_true = [1,0,1,1,0,0,1,0]
    y_pred = [1,0,0,1,0,1,1,0]

    r = evaluate_binary(y_true, y_pred)
    assert r["confusion"] == [[3,1],[1,3]]  # tn=3 fp=1 fn=1 tp=3
    assert abs(r["accuracy"] - 0.75) < 1e-9
    assert abs(r["precision"] - (3/4)) < 1e-9
    assert abs(r["recall"] - (3/4)) < 1e-9
    assert abs(r["f1"] - (3/4)) < 1e-9

def test_zero_denoms():
    r = evaluate_binary([0,0], [0,0])
    assert r["precision"] == 0.0
    assert r["recall"] == 0.0
    assert r["f1"] == 0.0

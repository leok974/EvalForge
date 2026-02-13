from task import ml_ready

def test_ml_ready_literal():
    assert ml_ready() == "ML_READY"

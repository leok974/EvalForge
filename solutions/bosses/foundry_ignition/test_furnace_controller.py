# test_furnace_controller.py

from furnace_controller import decide_action, compute_average


def test_decide_action_stable():
    assert decide_action(21.0, target_temp=21.0, tolerance=1.0) == "STABLE"
    assert decide_action(20.2, target_temp=21.0, tolerance=1.0) == "STABLE"
    assert decide_action(21.8, target_temp=21.0, tolerance=1.0) == "STABLE"


def test_decide_action_heat_vs_cool():
    assert decide_action(18.0, target_temp=21.0, tolerance=1.0) == "HEAT"
    assert decide_action(23.5, target_temp=21.0, tolerance=1.0) == "COOL"


def test_compute_average_basic():
    assert compute_average([20.0, 22.0]) == 21.0


def test_compute_average_empty_raises():
    import pytest

    with pytest.raises(ValueError):
        compute_average([])

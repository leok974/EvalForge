# test_data_crucible.py

from data_crucible import CrucibleConfig, aggregate


def test_crucible_config_from_dict_ok():
    data = {"group_by": ["month", "category"], "value_field": "amount"}
    cfg = CrucibleConfig.from_dict(data)
    assert cfg.group_by == ["month", "category"]
    assert cfg.value_field == "amount"


def test_aggregate_basic():
    rows = [
        {"month": "2025-11", "category": "food", "amount": "10.0"},
        {"month": "2025-11", "category": "food", "amount": "5.0"},
        {"month": "2025-11", "category": "rent", "amount": "1000.0"},
    ]

    result = aggregate(rows, group_by=["month", "category"], value_field="amount")

    # result is a list of dicts; easier to map for assertions
    key_map = {(r["month"], r["category"]): r for r in result}

    food = key_map[("2025-11", "food")]
    assert food["sum"] == 15.0
    assert food["count"] == 2
    assert food["avg"] == 7.5

    rent = key_map[("2025-11", "rent")]
    assert rent["sum"] == 1000.0
    assert rent["count"] == 1
    assert rent["avg"] == 1000.0


def test_aggregate_missing_group_column_raises():
    import pytest

    rows = [{"month": "2025-11", "amount": "10.0"}]  # no 'category'
    with pytest.raises(ValueError):
        aggregate(rows, group_by=["month", "category"], value_field="amount")

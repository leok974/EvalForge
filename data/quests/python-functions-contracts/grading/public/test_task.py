import pytest
from task import process_user_data

def test_valid_user():
    user = {"name": " Alice ", "age": 30}
    result = process_user_data(user)
    assert result["name"] == "Alice"
    assert result["age"] == 30
    assert result["active"] is True

def test_invalid_name():
    with pytest.raises(ValueError):
        process_user_data({"name": 123, "age": 30})
    with pytest.raises(ValueError):
        process_user_data({"age": 30})

def test_invalid_age():
    with pytest.raises(ValueError):
        process_user_data({"name": "Bob", "age": "30"})
    with pytest.raises(ValueError):
        process_user_data({"name": "Bob", "age": -5})

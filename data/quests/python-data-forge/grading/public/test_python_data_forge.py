import pytest
from main import forge_data

def test_forge_data():
    in_data = [
        {'id': 1, 'name': 'Alice', 'active': True},
        {'id': 2, 'name': 'Bob', 'active': False},
        {'id': 3, 'name': 'Charlie', 'active': True}
    ]
    out = forge_data(in_data)
    assert out == {1: 'Alice', 3: 'Charlie'}
    assert 2 not in out
import pytest
from main import generate_evens

def test_generate_evens():
    assert generate_evens(10) == [2, 4, 6, 8, 10]
    assert generate_evens(5) == [2, 4]
    assert generate_evens(1) == []
    assert generate_evens(2) == [2]
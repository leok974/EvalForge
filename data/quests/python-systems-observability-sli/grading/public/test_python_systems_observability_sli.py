import pytest
from main import calculate_sli

def test_sli():
    assert calculate_sli(99, 100) == 0.99
    assert calculate_sli(0, 0) == 1.0
    assert calculate_sli(50, 100) == 0.5
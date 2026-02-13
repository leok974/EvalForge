import pytest
from main import process_numbers

def test_process_numbers():
    assert process_numbers([1, 2, 3, 4]) == [4, 8]
    assert process_numbers([1, 3, 5]) == []
    assert process_numbers([]) == []
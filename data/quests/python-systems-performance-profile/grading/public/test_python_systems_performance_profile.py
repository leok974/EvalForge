import pytest
from main import profile_matrix

def test_matrix():
    assert profile_matrix(2) == [[1, 0], [0, 1]]
    assert profile_matrix(3) == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
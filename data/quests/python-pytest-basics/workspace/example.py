import pytest
from calculator import add

def test_add():
    assert add(2, 3) == 5

if __name__ == "__main__":
    pytest.main([__file__])

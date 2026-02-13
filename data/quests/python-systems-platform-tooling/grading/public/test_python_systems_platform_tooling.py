import pytest
from main import parse_semver

def test_semver():
    assert parse_semver("1.2.3") == (1, 2, 3)
    with pytest.raises(ValueError):
        parse_semver("1.2")
    with pytest.raises(ValueError):
        parse_semver("a.b.c")
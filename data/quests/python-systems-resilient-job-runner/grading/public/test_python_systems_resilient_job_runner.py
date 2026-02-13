import pytest
from unittest.mock import Mock
from main import run_with_retry

def test_success():
    m = Mock(return_value="ok")
    assert run_with_retry(m, 3) == "ok"
    assert m.call_count == 1

def test_retry_success():
    m = Mock(side_effect=[Exception("fail"), "ok"])
    assert run_with_retry(m, 3) == "ok"
    assert m.call_count == 2

def test_fail_all():
    m = Mock(side_effect=ValueError("boom"))
    with pytest.raises(ValueError):
        run_with_retry(m, 2)
    assert m.call_count == 3
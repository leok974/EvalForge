import pytest
from unittest.mock import Mock
from main import run_with_retries, RetryError


def test_success_first_try():
    m = Mock(return_value="ok")
    assert run_with_retries(m) == "ok"
    assert m.call_count == 1


def test_retry_then_success():
    m = Mock(side_effect=[Exception("transient"), "ok"])
    result = run_with_retries(m, max_attempts=3)
    assert result == "ok"
    assert m.call_count == 2


def test_all_fail_raises_retry_error():
    m = Mock(side_effect=ValueError("boom"))
    with pytest.raises(RetryError):
        run_with_retries(m, max_attempts=3)
    assert m.call_count == 3


def test_retry_error_chains_last_exception():
    cause = ValueError("root cause")
    m = Mock(side_effect=cause)
    with pytest.raises(RetryError) as exc_info:
        run_with_retries(m, max_attempts=2)
    assert exc_info.value.__cause__ is cause


def test_backoff_called_between_failures():
    sleep_calls = []
    m = Mock(side_effect=[Exception("x"), Exception("y"), "ok"])
    run_with_retries(
        m, max_attempts=3, backoff_seconds=1.0,
        sleep_fn=lambda t: sleep_calls.append(t)
    )
    assert sleep_calls == [1.0, 2.0]  # backoff_seconds * 2^0, 2^1


def test_no_sleep_on_first_success():
    sleep_calls = []
    m = Mock(return_value="done")
    run_with_retries(m, sleep_fn=lambda t: sleep_calls.append(t))
    assert sleep_calls == []

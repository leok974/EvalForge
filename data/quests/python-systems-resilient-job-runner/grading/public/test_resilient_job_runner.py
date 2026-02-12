import pytest

from workspace.task import run_with_retries, RetryError


def test_retries_then_succeeds():
  calls = {"n": 0}

  def job():
    calls["n"] += 1
    if calls["n"] < 3:
      raise RuntimeError("flaky")
    return "ok"

  sleeps: list[float] = []

  def fake_sleep(x: float) -> None:
    sleeps.append(x)

  result = run_with_retries(job, max_attempts=5, backoff_seconds=0.1, sleep_fn=fake_sleep)
  assert result == "ok"
  assert calls["n"] == 3
  assert sleeps == [0.1, 0.2]  # backoff doubles


def test_exhausts_and_raises_retryerror_with_cause():
  calls = {"n": 0}

  def job():
    calls["n"] += 1
    raise ValueError("always fails")

  def no_sleep(_: float) -> None:
    return None

  with pytest.raises(RetryError) as ei:
    run_with_retries(job, max_attempts=3, backoff_seconds=0.5, sleep_fn=no_sleep)

  assert calls["n"] == 3
  assert isinstance(ei.value.__cause__, ValueError)
  assert str(ei.value.__cause__) == "always fails"

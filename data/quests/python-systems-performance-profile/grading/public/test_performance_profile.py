import pytest

from workspace.task import most_common_tokens, main


def test_most_common_tokens_ordering():
  text = "b a A a b c c c"
  assert most_common_tokens(text, 3) == [("c", 3), ("a", 3), ("b", 2)]


def test_most_common_tokens_ignores_non_alpha():
  text = "ok! ok? error-ERROR 123 warn"
  assert most_common_tokens(text, 3) == [("ok", 2), ("error", 2), ("warn", 1)]


def test_main_output(capsys: pytest.CaptureFixture[str]):
  main()
  out = capsys.readouterr().out.strip().splitlines()
  assert out == ["error=3", "ok=2", "warn=1"]

import pytest

from workspace.task import main


def test_help_prints_usage(capsys: pytest.CaptureFixture[str]):
  code = main(["--help"])
  out = capsys.readouterr().out.strip()
  assert code == 0
  assert out == "usage: tool greet --name NAME | tool sum A B"


def test_greet_happy_path(capsys: pytest.CaptureFixture[str]):
  code = main(["greet", "--name", "Leo"])
  out = capsys.readouterr().out.strip()
  assert code == 0
  assert out == "Hello, Leo!"


def test_sum_happy_path(capsys: pytest.CaptureFixture[str]):
  code = main(["sum", "2", "5"])
  out = capsys.readouterr().out.strip()
  assert code == 0
  assert out == "a+b=7"


def test_invalid_args_return_2_and_usage(capsys: pytest.CaptureFixture[str]):
  code = main(["greet", "Leo"])
  out = capsys.readouterr().out.strip()
  assert code == 2
  assert out == "usage: tool greet --name NAME | tool sum A B"

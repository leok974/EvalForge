import pytest

from workspace.task import generate_evens, main


def test_generate_evens_basic():
  assert generate_evens(1) == []
  assert generate_evens(2) == [2]
  assert generate_evens(3) == [2]
  assert generate_evens(10) == [2, 4, 6, 8, 10]


def test_main_prints_expected(capsys: pytest.CaptureFixture[str]):
  main()
  out = capsys.readouterr().out.strip()
  assert out == "2,4,6,8,10"

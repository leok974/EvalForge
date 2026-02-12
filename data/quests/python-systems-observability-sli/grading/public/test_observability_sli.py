import pytest
from pathlib import Path
import json

from workspace.task import calculate_availability, main


def _events():
  path = Path(__file__).resolve().parents[2] / "fixtures" / "events.jsonl"
  return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_calculate_availability_fixture():
  events = _events()
  # Success codes: 200,204,302,200,200,200,201 => 7 successes out of 10
  assert calculate_availability(events) == 0.7


def test_calculate_availability_empty_is_1():
  assert calculate_availability([]) == 1.0


def test_main_prints_expected(capsys: pytest.CaptureFixture[str]):
  main()
  out = capsys.readouterr().out.strip()
  assert out == "availability=0.7000"

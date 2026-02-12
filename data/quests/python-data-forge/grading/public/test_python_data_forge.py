import pytest
from pathlib import Path

from workspace.task import load_sales, revenue_by_item, top_items, main


def _fixture_path() -> Path:
  # grading/public -> grading -> quest root
  return Path(__file__).resolve().parents[2] / "fixtures" / "sales.csv"


def test_load_sales_parses_types():
  rows = load_sales(_fixture_path())
  assert isinstance(rows, list)
  assert rows[0]["item"] == "apple"
  assert rows[0]["qty"] == 2
  assert pytest.approx(rows[0]["price"], rel=0, abs=1e-9) == 1.50


def test_revenue_by_item_and_top_items():
  rows = load_sales(_fixture_path())
  rev = revenue_by_item(rows)

  assert pytest.approx(rev["apple"], rel=0, abs=1e-9) == 10.50
  assert pytest.approx(rev["banana"], rel=0, abs=1e-9) == 6.40
  assert pytest.approx(rev["carrot"], rel=0, abs=1e-9) == 2.50

  assert top_items(rev, 2) == [("apple", 10.5), ("banana", 6.4)]


def test_main_prints_expected(capsys: pytest.CaptureFixture[str]):
  main()
  out = capsys.readouterr().out.strip().splitlines()
  assert out == ["apple=10.50", "banana=6.40"]

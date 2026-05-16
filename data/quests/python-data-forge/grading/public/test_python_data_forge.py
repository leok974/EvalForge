import pytest
from main import load_sales, revenue_by_item, top_items
from pathlib import Path


# Runner copies workspace + test files into same temp dir; fixture lives at ./fixtures/
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "sales.csv"


def _rows():
    # Fallback to CWD-relative path used by runner
    path = FIXTURE if FIXTURE.exists() else Path("fixtures/sales.csv")
    return load_sales(path)


def test_load_sales_returns_list():
    rows = _rows()
    assert isinstance(rows, list)
    assert len(rows) > 0


def test_load_sales_field_types():
    rows = _rows()
    for row in rows:
        assert isinstance(row["item"], str)
        assert isinstance(row["qty"], int)
        assert isinstance(row["price"], float)


def test_revenue_by_item_totals():
    rows = _rows()
    rev = revenue_by_item(rows)
    # apple: (2*1.50) + (1*1.50) + (4*1.50) = 10.50
    assert abs(rev.get("apple", 0) - 10.50) < 0.01
    # banana: (5*0.80) + (3*0.80) = 6.40
    assert abs(rev.get("banana", 0) - 6.40) < 0.01


def test_top_items_order():
    rows = _rows()
    rev = revenue_by_item(rows)
    top2 = top_items(rev, 2)
    assert len(top2) == 2
    # Apple has highest revenue
    assert top2[0][0] == "apple"
    assert abs(top2[0][1] - 10.50) < 0.01

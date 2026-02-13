import pytest
import pandas as pd
import os
from workspace.task import analyze_city_age

def test_analyze_city_age(tmp_path):
    # Create dummy csv
    csv = tmp_path / "data.csv"
    csv.write_text("city,age\nNY,30\nLA,40\nNY,50\nLA,20", encoding="utf-8")
    
    res = analyze_city_age(str(csv))
    
    assert res["LA"] == 30.0
    assert res["NY"] == 40.0
    assert list(res.index) == ["LA", "NY"]
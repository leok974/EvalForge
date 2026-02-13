from pathlib import Path
import pandas as pd
from task import load_people, average_age_by_city

def test_people_load_and_aggregate():
    quest_dir = Path(__file__).resolve().parents[2]
    csv_path = quest_dir / "fixtures" / "people.csv"
    df = load_people(str(csv_path))

    assert list(df.columns) == ["id", "name", "age", "city"]
    assert df.shape == (5, 4)

    s = average_age_by_city(df)
    assert isinstance(s, pd.Series)
    assert list(s.index) == ["Austin", "Chicago", "Detroit"]
    assert s.loc["Austin"] == 10.0
    assert s.loc["Chicago"] == 45.0
    assert s.loc["Detroit"] == 25.0

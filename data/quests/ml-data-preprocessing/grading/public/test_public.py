from pathlib import Path
import pandas as pd
from task import preprocess

def test_preprocess_impute_onehot_order():
    quest_dir = Path(__file__).resolve().parents[2]
    csv_path = quest_dir / "fixtures" / "raw.csv"
    df = pd.read_csv(csv_path)

    out = preprocess(df)

    expected_cols = ["age", "city__Austin", "city__Chicago", "city__Detroit", "city__Unknown"]
    assert list(out.columns) == expected_cols

    # median of [30,50,20,10] = (20+30)/2 = 25
    assert out["age"].isna().sum() == 0
    assert float(out.loc[1, "age"]) == 25.0
    assert float(out.loc[4, "age"]) == 25.0

    # unknown row
    assert int(out.loc[2, "city__Unknown"]) == 1

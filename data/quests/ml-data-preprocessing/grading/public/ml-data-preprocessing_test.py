import pytest
import pandas as pd
import numpy as np
from workspace.task import preprocess

def test_preprocess():
    df = pd.DataFrame({
        "age": [20, np.nan, 30],
        "city": ["NY", np.nan, "LA"]
    })
    # Median age = 25.0
    # City nan -> Unknown
    # One hot: city__LA, city__NY, city__Unknown
    res = preprocess(df)
    
    assert "city__Unknown" in res.columns
    assert res.loc[1, "age"] == 25.0
    assert res.loc[1, "city__Unknown"] == 1
    assert res.loc[0, "city__NY"] == 1
    
    # Check expected columns presence/order isn't strictly enforced by this simple test
    # but basic correctness is.
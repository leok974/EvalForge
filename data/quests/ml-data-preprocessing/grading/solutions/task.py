import pandas as pd

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    med = out["age"].dropna().median()
    out["age"] = out["age"].fillna(med)

    out["city"] = out["city"].fillna("Unknown")

    cats = sorted(out["city"].unique().tolist())
    dummies = pd.get_dummies(out["city"], prefix="city", prefix_sep="__")
    # Ensure all expected cats exist (including Unknown) and stable order
    expected = [f"city__{c}" for c in ["Austin", "Chicago", "Detroit", "Unknown"]]
    for col in expected:
        if col not in dummies.columns:
            dummies[col] = 0

    dummies = dummies[expected]
    out2 = pd.concat([out[["age"]], dummies], axis=1)
    return out2

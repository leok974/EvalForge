import pandas as pd

def load_people(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path)

def average_age_by_city(df: pd.DataFrame) -> pd.Series:
    s = df.groupby("city")["age"].mean().sort_index()
    return s

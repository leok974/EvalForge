import pandas as pd

def analyze_city_age(csv_path):
    df = pd.read_csv(csv_path)
    return df.groupby('city')['age'].mean().sort_index()
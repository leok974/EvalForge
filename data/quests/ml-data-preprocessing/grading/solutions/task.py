import pandas as pd
import numpy as np

def preprocess(df):
    df = df.copy()
    # Impute age
    median_age = df['age'].median()
    df['age'] = df['age'].fillna(median_age)
    
    # Impute city
    df['city'] = df['city'].fillna('Unknown')
    
    # One-hot
    df = pd.get_dummies(df, columns=['city'], prefix='city', prefix_sep='__')
    
    # Ensure booleans are standard ints/floats if needed, or leave as is
    # Using ints for consistency
    for col in df.columns:
        if col.startswith('city__'):
            df[col] = df[col].astype(int)
            
    return df
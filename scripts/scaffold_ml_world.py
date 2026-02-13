import json
import os
import shutil
from pathlib import Path

# User Specs
QUESTS_SPECS = [
    {
        "slug": "ml-ignition",
        "title": "ML Ignition",
        "student_task_summary": "Implement a deterministic readiness handshake.",
        "test_code": """
import pytest
from workspace.task import ignite

def test_ignition():
    assert ignite() == "READY", "Ignition failed: expected 'READY'"
""",
        "solution_py": """
def ignite():
    return "READY"
"""
    },
    {
        "slug": "ml-numpy-basics",
        "title": "Numpy Basics",
        "student_task_summary": "Normalize a 1D array using min-max scaling.",
        "test_code": """
import pytest
import numpy as np
from workspace.task import normalize

def test_normalize_simple():
    arr = np.array([10, 20, 30])
    res = normalize(arr)
    expected = np.array([0.0, 0.5, 1.0])
    np.testing.assert_allclose(res, expected, atol=1e-5)

def test_normalize_constant():
    arr = np.array([5, 5, 5])
    res = normalize(arr)
    expected = np.zeros(3)
    np.testing.assert_allclose(res, expected, atol=1e-5)
""",
        "solution_py": """
import numpy as np

def normalize(arr):
    arr = np.asarray(arr, dtype=float)
    mi, ma = arr.min(), arr.max()
    if mi == ma:
        return np.zeros_like(arr)
    return (arr - mi) / (ma - mi)
"""
    },
    {
        "slug": "ml-pandas-dataframes",
        "title": "Pandas Dataframes",
        "student_task_summary": "Load CSV and compute mean age by city.",
        "test_code": """
import pytest
import pandas as pd
import os
from workspace.task import analyze_city_age

def test_analyze_city_age(tmp_path):
    # Create dummy csv
    csv = tmp_path / "data.csv"
    csv.write_text("city,age\\nNY,30\\nLA,40\\nNY,50\\nLA,20", encoding="utf-8")
    
    res = analyze_city_age(str(csv))
    
    assert res["LA"] == 30.0
    assert res["NY"] == 40.0
    assert list(res.index) == ["LA", "NY"]
""",
        "solution_py": """
import pandas as pd

def analyze_city_age(csv_path):
    df = pd.read_csv(csv_path)
    return df.groupby('city')['age'].mean().sort_index()
"""
    },
    {
        "slug": "ml-data-preprocessing",
        "title": "Data Preprocessing",
        "student_task_summary": "Impute missing values and one-hot encode.",
        "test_code": """
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
""",
        "solution_py": """
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
"""
    },
    {
        "slug": "ml-train-test-split",
        "title": "Train Test Split",
        "student_task_summary": "Deterministic split using fixed seed.",
        "test_code": """
import pytest
import numpy as np
from workspace.task import split_data

def test_split_deterministic():
    X = np.arange(100).reshape(100, 1)
    y = np.arange(100)
    
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, seed=42)
    
    # Check sizes
    assert len(X_test) == 20
    assert len(X_train) == 80
    
    # Check determinism (repeating gives same result)
    X_tr2, X_te2, y_tr2, y_te2 = split_data(X, y, test_size=0.2, seed=42)
    np.testing.assert_array_equal(X_test, X_te2)
    np.testing.assert_array_equal(y_test, y_te2)
    
    # Check shuffle happened (highly likely)
    assert not np.array_equal(y_train, np.arange(80))
""",
        "solution_py": """
import numpy as np
import math

def split_data(X, y, test_size=0.2, seed=42):
    rng = np.random.default_rng(seed)
    n = len(X)
    n_test = math.ceil(n * test_size)
    
    indices = np.arange(n)
    rng.shuffle(indices)
    
    test_idx = indices[-n_test:]
    train_idx = indices[:-n_test]
    
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]
"""
    },
    {
        "slug": "ml-linear-regression",
        "title": "Linear Regression",
        "student_task_summary": "Implement closed-form linear regression.",
        "test_code": """
import pytest
import numpy as np
from workspace.task import fit_predict

def test_linear_regression():
    # Simple y = 2x
    X = np.array([[1], [2], [3]])
    y = np.array([2, 4, 6])
    coef, intercept, preds = fit_predict(X, y)
    
    np.testing.assert_allclose(coef, [2.0], atol=1e-5)
    np.testing.assert_allclose(intercept, 0.0, atol=1e-5)
    np.testing.assert_allclose(preds, y, atol=1e-5)
""",
        "solution_py": """
import numpy as np

def fit_predict(X, y):
    # Add bias
    X_b = np.c_[np.ones((len(X), 1)), X]
    # Normal equation: theta = pinv(X_b) @ y
    theta = np.linalg.pinv(X_b) @ y
    
    intercept = theta[0]
    coef = theta[1:]
    
    preds = X @ coef + intercept
    return coef, intercept, preds
"""
    },
    {
        "slug": "ml-classification-basics",
        "title": "Classification Basics",
        "student_task_summary": "Implement kNN classifier.",
        "test_code": """
import pytest
import numpy as np
from workspace.task import knn_predict

def test_knn():
    X_train = np.array([[0], [1], [2], [10], [11], [12]])
    y_train = np.array([0, 0, 0, 1, 1, 1])
    
    X_test = np.array([[0.5], [11.5]])
    
    preds = knn_predict(X_train, y_train, X_test, k=3)
    np.testing.assert_array_equal(preds, [0, 1])
""",
        "solution_py": """
import numpy as np

def knn_predict(X_train, y_train, X_test, k=3):
    preds = []
    for x in X_test:
        # Distances
        dists = np.sqrt(np.sum((X_train - x)**2, axis=1))
        # Nearest k indices
        idx = np.argsort(dists)[:k]
        # Vote
        labels = y_train[idx]
        counts = np.bincount(labels, minlength=2)
        # Tie break to 0 is implicit if counts equal and argmax picks first
        # But for strict determinism we can just use argmax which works
        preds.append(np.argmax(counts))
    return np.array(preds)
"""
    },
    {
        "slug": "ml-model-evaluation",
        "title": "Model Evaluation",
        "student_task_summary": "Compute accuracy, precision, recall, f1.",
        "test_code": """
import pytest
import numpy as np
from workspace.task import evaluate

def test_metrics():
    y_true = np.array([0, 1, 1, 1])
    y_pred = np.array([0, 0, 1, 1])
    # TP=2, FP=0, FN=1, TN=1
    # Acc = 3/4 = 0.75
    # Prec = 2/2 = 1.0
    # Rec = 2/3 = 0.666...
    # F1 = 2*1*0.66/(1+0.66) = 0.8
    
    metrics = evaluate(y_true, y_pred)
    
    assert metrics["accuracy"] == 0.75
    assert metrics["precision"] == 1.0
    assert abs(metrics["recall"] - 2/3) < 1e-5
    assert abs(metrics["f1"] - 0.8) < 1e-5
    np.testing.assert_array_equal(metrics["confusion_matrix"], [[1, 0], [1, 2]])
""",
        "solution_py": """
import numpy as np

def evaluate(y_true, y_pred):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    
    acc = (tp + tn) / len(y_true)
    
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    
    if (prec + rec) > 0:
        f1 = 2 * prec * rec / (prec + rec)
    else:
        f1 = 0.0
        
    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "confusion_matrix": [[tn, fp], [fn, tp]]
    }
"""
    },
    {
        "slug": "ml-neural-networks-intro",
        "title": "Neural Networks Intro",
        "student_task_summary": "Implement dense layer forward pass.",
        "test_code": """
import pytest
import numpy as np
from workspace.task import dense_forward

def test_dense_relu():
    X = np.array([[1, -1]])
    W = np.array([[1, 1], [0, 1]]) # (2,2)
    b = np.array([0, 1])
    # Z = X@W + b = [1, 0] + [0, 1] = [1, 1]
    # Relu([1, 1]) = [1, 1]
    
    out = dense_forward(X, W, b, activation="relu")
    np.testing.assert_array_equal(out, [[1, 1]])

def test_dense_sigmoid():
    X = np.array([[0, 0]])
    W = np.zeros((2,1))
    b = np.array([0])
    # Z = 0
    # Sigmoid(0) = 0.5
    out = dense_forward(X, W, b, activation="sigmoid")
    np.testing.assert_allclose(out, [[0.5]], atol=1e-5)
""",
        "solution_py": """
import numpy as np

def dense_forward(X, W, b, activation="relu"):
    Z = X @ W + b
    if activation == "relu":
        return np.maximum(0, Z)
    elif activation == "sigmoid":
        return 1 / (1 + np.exp(-Z))
    return Z
"""
    },
    {
        "slug": "ml-overfitting-regularization",
        "title": "Overfitting & Regularization",
        "student_task_summary": "Compute MSE with Ridge penalty.",
        "test_code": """
import pytest
import numpy as np
from workspace.task import ridge_loss

def test_ridge():
    y_true = np.array([1, 2])
    y_pred = np.array([1, 2]) # MSE = 0
    coef = np.array([1, -1])  # sum sq = 2
    alpha = 0.5
    
    # Loss = 0 + 0.5 * 2 = 1.0
    loss = ridge_loss(y_true, y_pred, coef, alpha)
    assert loss == 1.0
""",
        "solution_py": """
import numpy as np

def ridge_loss(y_true, y_pred, coef, alpha):
    mse = np.mean((y_true - y_pred)**2)
    penalty = alpha * np.sum(coef**2)
    return mse + penalty
"""
    }
]

def main():
    root = Path.cwd()
    quests_dir = root / "data" / "quests"
    
    for q in QUESTS_SPECS:
        slug = q["slug"]
        print(f"Scaffolding {slug}...")
        q_dir = quests_dir / slug
        
        # Paths
        ws_dir = q_dir / "workspace"
        grading_dir = q_dir / "grading"
        
        # Clean
        if ws_dir.exists(): shutil.rmtree(ws_dir)
        if grading_dir.exists(): shutil.rmtree(grading_dir)
        
        ws_dir.mkdir(parents=True, exist_ok=True)
        pub_dir = grading_dir / "public"
        sol_dir = grading_dir / "solutions"
        pub_dir.mkdir(parents=True, exist_ok=True)
        sol_dir.mkdir(parents=True, exist_ok=True)
        
        # README
        readme_txt = f"# {q['title']}\n\n{q['student_task_summary']}\n"
        (ws_dir / "README.md").write_bytes(readme_txt.encode("utf-8"))
        
        # Starter task.py
        starter_py = "# TODO: Implement\ndef task():\n    pass\n"
        (ws_dir / "task.py").write_bytes(starter_py.encode("utf-8"))
        
        # Tests
        test_txt = q["test_code"].replace("\r\n", "\n").strip()
        (pub_dir / f"{slug}_test.py").write_bytes(test_txt.encode("utf-8"))
        
        # Solution
        sol_txt = q["solution_py"].replace("\r\n", "\n").strip()
        (sol_dir / "task.py").write_bytes(sol_txt.encode("utf-8"))
    
    print("Done.")

if __name__ == "__main__":
    main()

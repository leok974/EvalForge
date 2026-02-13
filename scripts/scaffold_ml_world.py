from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
DATA_QUESTS = ROOT / "data" / "quests"

def w(rel: str, content: str):
    p = DATA_QUESTS / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.strip() + "\n")

if __name__ == "__main__":
    # --- Quest 1: ml-ignition ---
    w("ml-ignition/workspace/README.md", r"""
# ML Ignition — Deterministic Handshake

Implement a tiny "ready" contract for the ML world.

## Requirements
Implement `ml_ready()` in `task.py`:

- Returns the exact string: `ML_READY`
- No printing
- No randomness
""")
    w("ml-ignition/workspace/task.py", r"""
def ml_ready() -> str:
    # TODO: return the exact readiness string
    raise NotImplementedError
""")
    w("ml-ignition/grading/solutions/task.py", r"""
def ml_ready() -> str:
    return "ML_READY"
""")
    w("ml-ignition/grading/public/test_public.py", r"""
from task import ml_ready

def test_ml_ready_literal():
    assert ml_ready() == "ML_READY"
""")

    # --- Quest 2: ml-numpy-basics ---
    w("ml-numpy-basics/workspace/README.md", r"""
# NumPy Basics — Min/Max Normalization

Implement `normalize_minmax(x)`:

- Input: 1D numpy array
- Output: normalized to [0, 1] using min/max
- If all values equal, return zeros array of same shape
- Do not mutate input
""")
    w("ml-numpy-basics/workspace/task.py", r"""
import numpy as np

def normalize_minmax(x: np.ndarray) -> np.ndarray:
    # TODO
    raise NotImplementedError
""")
    w("ml-numpy-basics/grading/solutions/task.py", r"""
import numpy as np

def normalize_minmax(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x)
    xmin = float(np.min(x))
    xmax = float(np.max(x))
    if xmax == xmin:
        return np.zeros_like(x, dtype=float)
    return (x - xmin) / (xmax - xmin)
""")
    w("ml-numpy-basics/grading/public/test_public.py", r"""
import numpy as np
from task import normalize_minmax

def test_normalize_basic():
    x = np.array([2, 4, 6], dtype=float)
    out = normalize_minmax(x)
    assert np.allclose(out, np.array([0.0, 0.5, 1.0]))
    assert np.allclose(x, np.array([2, 4, 6], dtype=float))  # no mutation

def test_normalize_constant():
    x = np.array([3, 3, 3], dtype=float)
    out = normalize_minmax(x)
    assert np.allclose(out, np.array([0.0, 0.0, 0.0]))
""")

    # --- Quest 3: ml-pandas-dataframes ---
    w("ml-pandas-dataframes/workspace/README.md", r"""
# Pandas DataFrames — Load + Aggregate

You have `fixtures/people.csv`.

Implement:
- `load_people(csv_path) -> DataFrame`
- `average_age_by_city(df) -> Series` (mean age by city), sorted by city name ascending
""")
    w("ml-pandas-dataframes/workspace/task.py", r"""
import pandas as pd

def load_people(csv_path: str) -> pd.DataFrame:
    # TODO
    raise NotImplementedError

def average_age_by_city(df: pd.DataFrame) -> pd.Series:
    # TODO
    raise NotImplementedError
""")
    w("ml-pandas-dataframes/grading/solutions/task.py", r"""
import pandas as pd

def load_people(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path)

def average_age_by_city(df: pd.DataFrame) -> pd.Series:
    s = df.groupby("city")["age"].mean().sort_index()
    return s
""")
    w("ml-pandas-dataframes/fixtures/people.csv", """
id,name,age,city
1,Alice,30,Detroit
2,Bob,20,Detroit
3,Charlie,40,Chicago
4,Dana,50,Chicago
5,Evan,10,Austin
""")
    w("ml-pandas-dataframes/grading/public/test_public.py", r"""
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
""")

    # --- Quest 4: ml-data-preprocessing ---
    w("ml-data-preprocessing/workspace/README.md", r"""
# Data Preprocessing — Impute + One-Hot

Fixture: `fixtures/raw.csv`

Implement `preprocess(df) -> DataFrame`:

- Numeric column `age`: fill missing with median of non-missing
- Categorical column `city`: fill missing with "Unknown"
- One-hot encode `city` into columns `city__<value>` (stable alphabetical order of categories)
- Output columns order must be:
  - age
  - city__Austin
  - city__Chicago
  - city__Detroit
  - city__Unknown
""")
    w("ml-data-preprocessing/workspace/task.py", r"""
import pandas as pd

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    # TODO
    raise NotImplementedError
""")
    w("ml-data-preprocessing/grading/solutions/task.py", r"""
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
""")
    w("ml-data-preprocessing/fixtures/raw.csv", """
age,city
30,Detroit
,Chicago
50,
20,Chicago
,Detroit
10,Austin
""")
    w("ml-data-preprocessing/grading/public/test_public.py", r"""
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
""")

    # --- Quest 5: ml-train-test-split ---
    w("ml-train-test-split/workspace/README.md", r"""
# Train/Test Split — Deterministic

Implement `train_test_split(X, y, test_size, seed)`:

- X: numpy array shape (n, d)
- y: numpy array shape (n,)
- test_size: float in (0, 1)
- seed: int
- Shuffle indices using the seed, then take the last `ceil(n * test_size)` as test
- Return: (X_train, X_test, y_train, y_test)
""")
    w("ml-train-test-split/workspace/task.py", r"""
import numpy as np
from typing import Tuple

def train_test_split(
    X: np.ndarray,
    y: np.ndarray,
    test_size: float,
    seed: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    # TODO
    raise NotImplementedError
""")
    w("ml-train-test-split/grading/solutions/task.py", r"""
import numpy as np
import math
from typing import Tuple

def train_test_split(
    X: np.ndarray,
    y: np.ndarray,
    test_size: float,
    seed: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    X = np.asarray(X)
    y = np.asarray(y)
    n = X.shape[0]

    rs = np.random.RandomState(seed)
    idx = rs.permutation(n)

    n_test = int(math.ceil(n * float(test_size)))
    test_idx = idx[-n_test:]
    train_idx = idx[:-n_test]

    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]
""")
    w("ml-train-test-split/grading/public/test_public.py", r"""
import numpy as np
from task import train_test_split

def test_split_deterministic_and_aligned():
    X = np.arange(20).reshape(10, 2)
    y = np.arange(10)

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, seed=123)

    assert Xtr.shape == (7, 2)
    assert Xte.shape == (3, 2)
    assert ytr.shape == (7,)
    assert yte.shape == (3,)

    # alignment: first column /2 should equal label *2? Actually X rows are [2k,2k+1], so label k
    assert np.all((Xtr[:, 0] // 2) == ytr)
    assert np.all((Xte[:, 0] // 2) == yte)

    # determinism
    Xtr2, Xte2, ytr2, yte2 = train_test_split(X, y, test_size=0.3, seed=123)
    assert np.array_equal(Xtr, Xtr2)
    assert np.array_equal(Xte, Xte2)
    assert np.array_equal(ytr, ytr2)
    assert np.array_equal(yte, yte2)
""")

    # --- Quest 6: ml-linear-regression ---
    w("ml-linear-regression/workspace/README.md", r"""
# Linear Regression — Fit + Predict (Closed Form)

Implement:
- `fit_linear_regression(X, y) -> (coef, intercept)`
- `predict_linear(X, coef, intercept) -> preds`

Where:
- X: numpy array (n, d)
- y: numpy array (n,)
- coef: numpy array (d,)
- intercept: float

Use a deterministic closed-form solution (pseudo-inverse is acceptable).
""")
    w("ml-linear-regression/workspace/task.py", r"""
import numpy as np
from typing import Tuple

def fit_linear_regression(X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, float]:
    # TODO
    raise NotImplementedError

def predict_linear(X: np.ndarray, coef: np.ndarray, intercept: float) -> np.ndarray:
    # TODO
    raise NotImplementedError
""")
    w("ml-linear-regression/grading/solutions/task.py", r"""
import numpy as np
from typing import Tuple

def fit_linear_regression(X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, float]:
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)

    # Add bias column
    Xb = np.concatenate([np.ones((X.shape[0], 1)), X], axis=1)
    w = np.linalg.pinv(Xb) @ y  # (d+1,)
    intercept = float(w[0])
    coef = w[1:]
    return coef, intercept

def predict_linear(X: np.ndarray, coef: np.ndarray, intercept: float) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    coef = np.asarray(coef, dtype=float)
    return X @ coef + float(intercept)
""")
    w("ml-linear-regression/grading/public/test_public.py", r"""
import numpy as np
from task import fit_linear_regression, predict_linear

def test_fit_predict_line():
    # y = 2*x + 1 exactly
    X = np.array([[0.0], [1.0], [2.0], [3.0]])
    y = np.array([1.0, 3.0, 5.0, 7.0])

    coef, intercept = fit_linear_regression(X, y)
    assert coef.shape == (1,)
    assert abs(intercept - 1.0) < 1e-9
    assert abs(coef[0] - 2.0) < 1e-9

    preds = predict_linear(np.array([[4.0], [5.0]]), coef, intercept)
    assert np.allclose(preds, np.array([9.0, 11.0]))
""")

    # --- Quest 7: ml-classification-basics ---
    w("ml-classification-basics/workspace/README.md", r"""
# Classification Basics — kNN (Deterministic)

Implement a tiny k-Nearest Neighbors classifier:

- `fit_knn(X_train, y_train, k)` returns a model dict
- `predict_knn(model, X)` returns predicted labels (0/1) using:
  - Euclidean distance
  - Majority vote
  - Ties break toward label 0 (deterministic)

All inputs are numpy arrays.
""")
    w("ml-classification-basics/workspace/task.py", r"""
import numpy as np
from typing import Dict, Any

def fit_knn(X_train: np.ndarray, y_train: np.ndarray, k: int) -> Dict[str, Any]:
    # TODO
    raise NotImplementedError

def predict_knn(model: Dict[str, Any], X: np.ndarray) -> np.ndarray:
    # TODO
    raise NotImplementedError
""")
    w("ml-classification-basics/grading/solutions/task.py", r"""
import numpy as np
from typing import Dict, Any

def fit_knn(X_train: np.ndarray, y_train: np.ndarray, k: int) -> Dict[str, Any]:
    return {
        "X_train": np.asarray(X_train, dtype=float),
        "y_train": np.asarray(y_train, dtype=int),
        "k": int(k),
    }

def predict_knn(model: Dict[str, Any], X: np.ndarray) -> np.ndarray:
    X_train = model["X_train"]
    y_train = model["y_train"]
    k = int(model["k"])

    X = np.asarray(X, dtype=float)
    preds = []
    for x in X:
        d2 = np.sum((X_train - x) ** 2, axis=1)
        idx = np.argsort(d2)[:k]
        votes = y_train[idx]
        ones = int(np.sum(votes == 1))
        zeros = k - ones
        preds.append(1 if ones > zeros else 0)  # tie -> 0
    return np.array(preds, dtype=int)
""")
    w("ml-classification-basics/grading/public/test_public.py", r"""
import numpy as np
from task import fit_knn, predict_knn

def test_knn_predicts_expected():
    X_train = np.array([[0,0],[0,1],[1,0],[1,1],[10,10],[10,11],[11,10],[11,11]], dtype=float)
    y_train = np.array([0,0,0,0, 1,1,1,1], dtype=int)

    model = fit_knn(X_train, y_train, k=3)
    X = np.array([[0.2,0.2], [10.2,10.2], [5,5]], dtype=float)

    pred = predict_knn(model, X)
    assert pred.tolist() == [0, 1, 0]  # middle is ambiguous but closer to cluster 0 with k=3 + tie rule
""")

    # --- Quest 8: ml-model-evaluation ---
    w("ml-model-evaluation/workspace/README.md", r"""
# Model Evaluation — Binary Metrics

Implement `evaluate_binary(y_true, y_pred)` returning a dict:

{
  "accuracy": float,
  "precision": float,
  "recall": float,
  "f1": float,
  "confusion": [[tn, fp],[fn, tp]]
}

Rules:
- Positive label is 1
- If precision or recall denom is 0, return 0.0 for that metric
""")
    w("ml-model-evaluation/workspace/task.py", r"""
from typing import Dict, List

def evaluate_binary(y_true: List[int], y_pred: List[int]) -> Dict:
    # TODO
    raise NotImplementedError
""")
    w("ml-model-evaluation/grading/solutions/task.py", r"""
from typing import Dict, List

def evaluate_binary(y_true: List[int], y_pred: List[int]) -> Dict:
    if len(y_true) != len(y_pred):
        raise ValueError("length mismatch")

    tn = fp = fn = tp = 0
    for yt, yp in zip(y_true, y_pred):
        if yt == 1 and yp == 1:
            tp += 1
        elif yt == 0 and yp == 0:
            tn += 1
        elif yt == 0 and yp == 1:
            fp += 1
        elif yt == 1 and yp == 0:
            fn += 1

    acc = (tp + tn) / len(y_true) if y_true else 0.0
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) else 0.0

    return {
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1": float(f1),
        "confusion": [[tn, fp], [fn, tp]],
    }
""")
    w("ml-model-evaluation/grading/public/test_public.py", r"""
from task import evaluate_binary

def test_metrics_and_confusion():
    y_true = [1,0,1,1,0,0,1,0]
    y_pred = [1,0,0,1,0,1,1,0]

    r = evaluate_binary(y_true, y_pred)
    assert r["confusion"] == [[3,1],[1,3]]  # tn=3 fp=1 fn=1 tp=3
    assert abs(r["accuracy"] - 0.75) < 1e-9
    assert abs(r["precision"] - (3/4)) < 1e-9
    assert abs(r["recall"] - (3/4)) < 1e-9
    assert abs(r["f1"] - (3/4)) < 1e-9

def test_zero_denoms():
    r = evaluate_binary([0,0], [0,0])
    assert r["precision"] == 0.0
    assert r["recall"] == 0.0
    assert r["f1"] == 0.0
""")

    # --- Quest 9: ml-neural-networks-intro ---
    w("ml-neural-networks-intro/workspace/README.md", r"""
# Neural Nets Intro — Dense Forward Pass

Implement `dense_forward(X, W, b, activation)`:

- X: (n, d)
- W: (d, h)
- b: (h,)
- activation: "relu" or "sigmoid"
- Returns: (n, h)

Use numpy only.
""")
    w("ml-neural-networks-intro/workspace/task.py", r"""
import numpy as np

def dense_forward(X: np.ndarray, W: np.ndarray, b: np.ndarray, activation: str) -> np.ndarray:
    # TODO
    raise NotImplementedError
""")
    w("ml-neural-networks-intro/grading/solutions/task.py", r"""
import numpy as np

def dense_forward(X: np.ndarray, W: np.ndarray, b: np.ndarray, activation: str) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    W = np.asarray(W, dtype=float)
    b = np.asarray(b, dtype=float)

    Z = X @ W + b
    if activation == "relu":
        return np.maximum(0.0, Z)
    if activation == "sigmoid":
        return 1.0 / (1.0 + np.exp(-Z))
    raise ValueError("activation must be 'relu' or 'sigmoid'")
""")
    w("ml-neural-networks-intro/grading/public/test_public.py", r"""
import numpy as np
from task import dense_forward

def test_dense_relu():
    X = np.array([[1, 2]], dtype=float)         # (1,2)
    W = np.array([[1, -1], [2, 0]], dtype=float) # (2,2)
    b = np.array([0.5, -0.5], dtype=float)      # (2,)

    out = dense_forward(X, W, b, "relu")
    # Z = [1*1+2*2+0.5, 1*-1+2*0-0.5] = [5.5, -1.5] -> relu => [5.5, 0]
    assert np.allclose(out, np.array([[5.5, 0.0]]))

def test_dense_sigmoid_shape():
    X = np.array([[0, 0],[1,1]], dtype=float)
    W = np.ones((2,3), dtype=float)
    b = np.zeros((3,), dtype=float)
    out = dense_forward(X, W, b, "sigmoid")
    assert out.shape == (2,3)
    assert np.all((out >= 0.0) & (out <= 1.0))
""")

    # --- Quest 10: ml-overfitting-regularization ---
    w("ml-overfitting-regularization/workspace/README.md", r"""
# Regularization — Ridge Loss

Implement `ridge_loss(y_true, y_pred, coef, alpha)`:

- MSE = mean((y_true - y_pred)^2)
- penalty = alpha * sum(coef^2)
- return MSE + penalty

All inputs are numpy arrays.
""")
    w("ml-overfitting-regularization/workspace/task.py", r"""
import numpy as np

def ridge_loss(y_true: np.ndarray, y_pred: np.ndarray, coef: np.ndarray, alpha: float) -> float:
    # TODO
    raise NotImplementedError
""")
    w("ml-overfitting-regularization/grading/solutions/task.py", r"""
import numpy as np

def ridge_loss(y_true: np.ndarray, y_pred: np.ndarray, coef: np.ndarray, alpha: float) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    coef = np.asarray(coef, dtype=float)

    mse = float(np.mean((y_true - y_pred) ** 2))
    penalty = float(alpha) * float(np.sum(coef ** 2))
    return mse + penalty
""")
    w("ml-overfitting-regularization/grading/public/test_public.py", r"""
import numpy as np
from task import ridge_loss

def test_ridge_loss_value():
    y_true = np.array([1.0, 2.0, 3.0])
    y_pred = np.array([1.0, 2.5, 2.0])
    coef = np.array([2.0, -1.0])
    alpha = 0.1

    mse = ((0.0**2) + (0.5**2) + (-1.0**2)) / 3.0  # (0 + 0.25 + 1)/3 = 0.416666...
    penalty = 0.1 * (4 + 1)  # 0.5
    expected = mse + penalty

    out = ridge_loss(y_true, y_pred, coef, alpha)
    assert abs(out - expected) < 1e-12
""")

import numpy as np

def normalize_minmax(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x)
    xmin = float(np.min(x))
    xmax = float(np.max(x))
    if xmax == xmin:
        return np.zeros_like(x, dtype=float)
    return (x - xmin) / (xmax - xmin)

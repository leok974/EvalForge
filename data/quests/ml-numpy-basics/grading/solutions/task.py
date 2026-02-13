import numpy as np

def normalize(arr):
    arr = np.asarray(arr, dtype=float)
    mi, ma = arr.min(), arr.max()
    if mi == ma:
        return np.zeros_like(arr)
    return (arr - mi) / (ma - mi)
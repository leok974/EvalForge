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
# Regularization — Ridge Loss

Implement `ridge_loss(y_true, y_pred, coef, alpha)`:

- MSE = mean((y_true - y_pred)^2)
- penalty = alpha * sum(coef^2)
- return MSE + penalty

All inputs are numpy arrays.

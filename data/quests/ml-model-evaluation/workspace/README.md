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

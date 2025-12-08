# Boss: Gradient Sentinel – Golden ML Training & Evaluation Incident Runbook

Scenario: A binary classifier (risky vs safe) looks great offline but underperforms in production. A recent retrain made false negatives worse.

---

## Incident Context

- **Task:** Binary classification – label each request as `risky` or `safe`.
- **Model:** Gradient-boosted tree or shallow neural network (architecture not critical).
- **Offline state:**
  - AUC and accuracy on the validation set are high.
  - Calibration plot *looks* reasonable at first glance.
- **Production state:**
  - Observed false negative rate (risky but predicted safe) is too high.
  - Complaint: “We are letting too many risky events through.”
- **Recent change:**
  - A retraining run one month ago increased offline metrics slightly but worsened production behavior.

**Goal:**  
Audit the data and training loop, fix evaluation, and define a safer training + monitoring plan.

---

## Phase 1 – Verify Data & Splits

1. **Check label distribution and leakage**

   - Compute overall label distribution (offline data):

```python
import pandas as pd

df = load_training_dataframe()
print(df["label"].value_counts(normalize=True))
```

* Inspect key ID/temporal fields:

  * `user_id`, `session_id`, `request_ts`, `country`, etc.

2. **Validate train/val/test construction**

   * If the task is temporal (requests over time), ensure **time-based splits**:

```python
df = df.sort_values("request_ts")
train = df[df["request_ts"] < "2025-09-01"]
val   = df[(df["request_ts"] >= "2025-09-01") & (df["request_ts"] < "2025-10-01")]
test  = df[df["request_ts"] >= "2025-10-01"]
```

* Confirm no user/session leakage:

```python
leak_users = set(train["user_id"]) & set(val["user_id"])
print("Leak users:", len(leak_users))
```

* If there is leakage:

  * Redesign splits by **user_id** or **time window**.

3. **Compare distribution of features across splits**

   * For key features (e.g., request amount, country, channel), compare histograms and summary stats between train/val/test and recent production data.
   * If distribution mismatch is severe, note this for Phase 5.

---

## Phase 2 – Inspect Metrics & Curves

4. **Review training curves**

   * Plot training vs validation loss and AUC:

```python
plot_training_curves(training_logs)
```

* Check for:

  * Overfitting: training loss down, validation loss up.
  * Underfitting: both flat and mediocre.
  * Instability: spikes, NaNs, or sudden drops.

5. **Examine class-specific metrics**

   * For this risk detection problem, focus on **recall / FNR for risky class**:

```python
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve

y_val = val["label"]
y_scores = model.predict_proba(val_features)[:, 1]

# Risky = 1
print(classification_report(y_val, y_scores > 0.5))
```

* If FNR is too high, we may need:

  * Different threshold,
  * Different loss weighting,
  * Or better features/splits.

6. **Check calibration**

   * Plot calibration curve per bucket of predicted probability.
   * Compare with production observations if available.

---

## Phase 3 – Stabilize & Improve Training

7. **Fix splits and re-train simple baselines**

   * Start with a **logistic regression baseline** and a **small tree model**:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# Baseline 1
log_reg = LogisticRegression(max_iter=1000, class_weight="balanced")
log_reg.fit(train_X, train_y)

# Baseline 2
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=8,
    class_weight="balanced",
    n_jobs=-1,
)
rf.fit(train_X, train_y)
```

* Evaluate baselines on clean val/test splits with metrics focused on recall and precision for the risky class.

8. **Adjust loss weighting and threshold**

   * Use class weights or focal loss to penalize false negatives more.
   * Choose a threshold optimized for the desired tradeoff:

```python
from sklearn.metrics import precision_recall_curve

precision, recall, thresholds = precision_recall_curve(y_val, y_scores)
# Select threshold targeting desired recall for risky = 1
```

* Document the chosen threshold and the rationale.

9. **Stabilize the training loop**

   * Check:

     * Learning rate not too high (if using NN).
     * No data shuffling bugs.
     * Consistent preprocessing between train/val/test.

   * If using deep models:

     * Use smaller architectures initially.
     * Add early stopping on validation loss/metric.

---

## Phase 4 – Baseline & Experiment Design

10. **Define baselines and experiment matrix**

* Baseline A: Logistic regression with cleaned splits + class_weight.
* Baseline B: Gradient-boosted tree with default parameters + class_weight.
* Experiment 1: Add selected engineered features (e.g., user history features).
* Experiment 2: Try different thresholds / decision rules.

11. **Use structured ablations**

* For each experiment:

  * Change one thing at a time.
  * Log metrics: FNR for risky class, precision, AUC, calibration error.
* Compare against baselines; record results in a simple table or CSV.

12. **Promotion criteria**

* Only promote an experiment if:

  * It improves target metrics (e.g., FNR & precision tradeoff) on held-out test.
  * It does not overfit (no big gap between val and test).
* Document criteria and decisions.

---

## Phase 5 – Production Monitoring & Retraining

13. **Align offline evaluation with production**

* Collect a sample of recent production events with ground truth (if available).
* Evaluate the current and candidate models on this **prod-like holdout**.

14. **Define monitoring metrics**

* For production:

  * Overall and segment-wise:

    * Predicted risk score distribution.
    * Fraction of traffic flagged as risky.
    * Estimated false negative / false positive rates (where labels are available).
    * Calibration drift signals (e.g., Brier score on labeled subset).

* Implement dashboards/alerts for:

  * Sudden changes in risk score distribution,
  * Sharp drops in recall for the risky class.

15. **Retraining strategy**

* Define:

  * Data window (e.g., last N months).
  * Retraining cadence (e.g., monthly, or triggered by drift metrics).
  * Validation protocol: retrain → evaluate vs baseline → canary → promote.

* Always compare new model to baseline in both offline and prod-like eval before promotion.

16. **Rollback plan**

* Keep the previous model available for quick rollback.
* Document:

  * How to revert to the previous model.
  * How to disable a bad model quickly if alerts fire.

This runbook focuses on **splits, diagnostics, baselines, and production safety**—what the Gradient Sentinel expects for a strong answer.

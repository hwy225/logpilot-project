# Overrun Watch — Task & Strategy

Purpose
-------
Summarize the task, approach, and implementation strategy for "Overrun Watch: Early-Warning Signals (Classification)". This document is the single-source plan for feature engineering, targets, modeling, evaluation, deliverables, and next steps.

Goals
-----
- Predict next-period overrun risk (time and/or cost) using lagged telemetry.
- Produce actionable alerts with lead time ≥ 1 period.
- Achieve AUC ≥ 0.75 on a holdout set and strong Precision@k for top alerts.

Deliverables
------------
- `models/overrun_classifier.ipynb`: analysis + modeling notebook
- `models/overrun_api.py`: production-ready predict function (loads model, validates features, returns probability + explanation)
- `task_and_strategy.md`: (this file) plan and strategy
- One-pager for PMs (problem, approach, metrics, limits)
- Stretch: calibrated probabilities + cost-aware thresholding

Data sources
------------
- `construction_project_dataset.csv` (primary) — contains `time_deviation`, `cost_deviation`, telemetry (temperature, humidity, vibration, energy, worker_count, material_usage, equipment_utilization_rate, task_progress, etc.)
- `construction_project_performance_dataset.csv` — additional sensor-level/performance telemetry; may require schema alignment and deduplication

High-level approach
-------------------
1. EDA & KPI discovery — find leading indicators and distributions
2. Feature engineering — create lag features (t-1..t-3), rolling stats, deltas, and derived KPIs
3. Target definition — binary labels for next-period time and cost overrun (and optional combined target)
4. Time-aware train/validation/test split — avoid leakage
5. Train baselines: Logistic Regression (interpretable) and XGBoost (strong non-linear baseline)
6. Evaluate by AUC, Precision@k, and lead-time performance; analyze SHAP explanations
7. Export model and build `overrun_api.py`; produce one-pager

Feature engineering (candidate features)
----------------------------------------
Start by exploring correlations and temporal lead/lag relationships. Candidate features to compute and test:
- Equipment metrics
  - `equipment_utilization_rate` (t, t-1, t-2, t-3)
  - `worker_count` and `energy_consumption / worker_count` (density/intensity)
  - `material_usage` and change in material usage
- Operational stress
  - `vibration_level` (lags, rolling mean, rolling std)
  - `safety_incidents` (count, recent window)
- Environment
  - `temperature`, `humidity` (lags)
- Progress & schedule
  - `task_progress` and `task_progress_velocity = task_progress_t - task_progress_t-1`
- Aggregates/Windows
  - rolling mean/std over last 3 or 7 periods for key signals
  - delta features: `x_t - x_t-1`

Feature forms to produce for each selected KPI:
- KPI_t, KPI_t-1, KPI_t-2, KPI_t-3
- KPI_rolling_mean_3, KPI_rolling_std_3
- KPI_delta_1 (t - t-1), KPI_trend (slope over last 3)
- Interaction candidate: `energy_per_worker = energy_consumption / max(1, worker_count)`

Target definitions
------------------
Options: separate targets for time and cost overruns (recommended):
- `time_overrun_next = 1 if time_deviation.shift(-1) > TH_time else 0`
- `cost_overrun_next = 1 if cost_deviation.shift(-1) > TH_cost else 0`

Threshold selection strategies:
- Percentile-based (e.g., top 25% = overrun) — quick, data-driven
- Business-defined (e.g., > 5% delay or > $X cost) — preferred if business input exists
- Multi-tier severity (low/medium/high) — optional later

Recommendation: start with percentile-based thresholds for experiments (e.g., 75th percentile). Record results and then switch to business thresholds when available.

Modeling plan
-------------
- Time-based split: train/val/test in chronological order (e.g., 70% / 15% / 15%) to preserve temporal dynamics and avoid leakage.
- Baselines:
  - Logistic Regression (L2, with class weighting or balanced sampling)
  - XGBoost classifier (early stopping on validation AUC)
- Hyperparameter tuning: grid or randomized search for XGBoost; regularization parameter for LR

Evaluation metrics (priority order)
----------------------------------
1. Precision@k (top-k alerts) — highest priority for PM actionability
2. AUC-ROC (target ≥ 0.75)
3. Recall / F1 (secondary; tradeoff with precision)
4. Calibration (Brier score) — for stretch goal
5. Lead-time validation — confirm predictions refer to next period (or more)

Interpretability & diagnostics
------------------------------
- SHAP summary plots for XGBoost to show feature contribution distribution
- Coefficients and odds ratios for Logistic Regression
- Error analysis: analyze false positives and false negatives by time, project phase, or sensor conditions

API contract (for `models/overrun_api.py`)
-----------------------------------------
Inputs:
- A dict or DataFrame row containing the current timestamp and required features (including lags and derived features), or raw telemetry with a helper to compute lags
- Model type selector: `target='time'|'cost'|'both'`

Outputs:
- `probability`: float (0..1)
- `label`: binary (1 if probability >= threshold)
- `explanation`: top contributing features (SHAP values summary)
- `metadata`: model version, timestamp, input checksum

Errors & validation:
- Validate required fields and lag availability; return meaningful error messages if features missing

Implementation & file layout
----------------------------
- `models/overrun_classifier.ipynb`: EDA -> feature engineering -> model training -> evaluation -> SHAP
- `models/overrun_api.py`: predict function, model loader, feature validator
- `models/` folder: store trained model artifacts (e.g., `xgb_time.pkl`, `lr_cost.pkl`) and transformers (scalers, encoders)
- `notebooks/` (optional): smaller exploratory notebooks

Contract & success criteria (short)
-----------------------------------
- Inputs: time series telemetry aggregated at chosen frequency (hourly/daily)
- Outputs: next-period overrun probability for time and cost
- Success: AUC ≥ 0.75 on holdout + acceptable Precision@k for actionable alerts
- Error modes: missing lag features, heavy class imbalance, concept drift over time

Edge cases & risks
------------------
- Class imbalance: overruns are likely rare — use class weights or resampling carefully
- Data leakage: ensure no future data in features; compute targets by forward-shift
- Non-stationarity & concept drift: model performance may degrade over time; establish monitoring
- Missing sensor data / dropped periods: handle with forward/backfill policies or explicit missing flags

Stretch goals
-------------
- Probability calibration (Platt scaling or isotonic regression)
- Cost-aware thresholding: pick threshold that optimizes expected business savings (alerts cost vs savings)
- Multi-period forecasting (2–3 periods ahead)
- Diagnostic & prescriptive suggestions (root-cause and recommended actions)

Next steps (immediate)
----------------------
1. Run EDA & KPI correlation analysis to choose top candidate KPIs and sensible thresholds (mark: EDA & KPI exploration)
2. Implement lag feature generator and a test harness that ensures no leakage
3. Train baseline LR and XGBoost on the time target; evaluate

Contacts & assumptions
----------------------
- Assumes data contains `time_deviation` and `cost_deviation` usable to form next-period targets
- Assumes telemetry timestamps are consistent (timezone-normalized) and can be resampled if needed

QA checklist before shipping
---------------------------
- [ ] Time-based train/val/test split used
- [ ] No feature leakage (no future data used in training)
- [ ] AUC and Precision@k reported for both targets
- [ ] SHAP explanation exported
- [ ] API returns validated output and explanation


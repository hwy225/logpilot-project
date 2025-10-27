# KPI Dictionary

This document defines the key performance indicators (KPIs) and data quality metrics 
used in the construction project analytics system.



## 🧮 1. Core Performance KPIs

| KPI Name | Definition | Formula / Logic | Unit | Source Columns | Example Python Snippet |
|:---|:---|:---|:---|:---|:---|
| **Average Cost Deviation** | Average deviation from planned cost | mean(`cost_deviation`) | % | cost_deviation | `df['cost_deviation'].mean()` |
| **Max Cost Deviation** | Max deviation from planned cost | mean(`cost_deviation`) | % | cost_deviation | `df['cost_deviation'].max()` |
| **Average Time Deviation** | Average delay (or ahead) vs schedule | mean(`time_deviation`) | % | time_deviation | `df['time_deviation'].mean()` |
| **Max Time Deviation** | Max delay (or ahead) vs schedule | mean(`time_deviation`) | % | time_deviation | `df['time_deviation'].max()` |
| **Equipment utilization** | Average utilization of machinery | mean(`equipment_utilization_rate`) | % | equipment_utilization_rate | `df['equipment_utilization_rate'].mean()` |
| **Energy / Worker Intensity** | Total energy use per worker | `energy_consumption` / `worker_count` | kWh/worker | energy_consumption, worker_count | `df['energy_consumption'] / df['worker_count']` |
| **Task progress velocity** | Change in task_progress over time | Δ(`task_progress`) | % per day/week | task_progress | `df['task_progress_last'] - df['task_progress_first']` |




## 🧰 2. Data Health Metrics

| Metric | Definition | Formula / Logic |
|:---|:---|:---|
| **missing_ratio** | Fraction of missing values per column | `df.isna().sum().sum() / df.size` |
| **outlier_ratio** | Fraction of values beyond 3σ | count($|x-μ|>3σ$)/n |
| **gap_ratio** | Gaps larger than expected in timestamp sequence | Δtimestamp > expected_interval |
| **invalid_ratio** | Negative or unrealistic values (e.g. worker_count < 0) | Boolean flag |
| **data_health_index** | Composite index of data quality | 100 - (weighted sum of above error rates) |

Example Python snippet:
```python
# ---- Data Health Checks ----
total_cells = df.size
missing_ratio = df.isna().sum().sum() / total_cells

# outliers：Z-score > 3
num_cols = ['temperature', 'humidity', 'vibration_level', 'material_usage',
    'worker_count', 'energy_consumption',
    'cost_deviation', 'time_deviation',
    'equipment_utilization_rate', 'material_shortage_alert', 'risk_score'
        ]
zscores = np.abs((df[num_cols] - df[num_cols].mean()) / df[num_cols].std())
outlier_ratio = (zscores > 3).sum().sum() / total_cells

# timestamp gaps
df = df.set_index('timestamp').sort_index()
expected = pd.date_range(df.index.min(), df.index.max(), freq='Min')
gap_ratio = 1 - len(df.index.unique()) / len(expected)

# improbable values check
invalid_conditions = (
    (df['task_progress'] < 0) | (df['task_progress'] > 100) |
    (df['worker_count'] < 0) | (df['energy_consumption'] < 0) |
    (df['equipment_utilization_rate'] < 0) | (df['equipment_utilization_rate'] > 100) |
    (df['risk_score'] < 0) | (df['risk_score'] > 100)
)
invalid_ratio = invalid_conditions.sum() / len(df)

# data health index
data_health_index = np.mean([
    1 - missing_ratio,
    1 - outlier_ratio,
    1 - gap_ratio,
    1 - invalid_ratio
])
```
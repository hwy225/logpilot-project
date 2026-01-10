# KPI Dictionary - Construction Project Analytics

## Overview

This document defines all Key Performance Indicators (KPIs) computed by the LogPilot system for construction project monitoring and decision support.

---

## Core KPIs

### 📊 Cost Metrics

#### `cost_deviation_avg`
- **Name**: Average Cost Deviation
- **Definition**: Mean deviation from budgeted costs over the aggregation period
- **Formula**: `AVG(cost_deviation)`
- **Unit**: Currency (project currency)
- **Interpretation**: 
  - Positive value = Over budget
  - Negative value = Under budget
  - Target: Close to 0
- **Python**:
  ```python
  cost_deviation_avg = df.groupby(period)['cost_deviation'].mean()
  ```

#### `cost_deviation_max`
- **Name**: Maximum Cost Deviation
- **Definition**: Largest absolute cost deviation in the period
- **Formula**: `MAX(cost_deviation)`
- **Unit**: Currency
- **Interpretation**: Peak budget variance, indicates worst-case cost management
- **Python**:
  ```python
  cost_deviation_max = df.groupby(period)['cost_deviation'].max()
  ```

#### `cost_efficiency`
- **Name**: Cost Efficiency Score
- **Definition**: Normalized inverse of cost deviation (0-100 scale)
- **Formula**: `100 - (|cost_deviation_avg| / max_deviation * 100)`
- **Unit**: Score (0-100)
- **Interpretation**:
  - 100 = Perfect budget adherence
  - 50 = Moderate variance
  - 0 = Maximum variance
- **Python**:
  ```python
  max_dev = abs(cost_deviation_avg).max()
  cost_efficiency = 100 - (abs(cost_deviation_avg) / max_dev * 100)
  ```

---

### ⏰ Schedule Metrics

#### `time_deviation_avg`
- **Name**: Average Time Deviation
- **Definition**: Mean deviation from planned schedule
- **Formula**: `AVG(time_deviation)`
- **Unit**: Days
- **Interpretation**:
  - Positive = Ahead of schedule
  - Negative = Behind schedule
  - Target: ≥ 0
- **Python**:
  ```python
  time_deviation_avg = df.groupby(period)['time_deviation'].mean()
  ```

#### `time_deviation_max`
- **Name**: Maximum Time Deviation
- **Definition**: Largest schedule deviation in the period
- **Formula**: `MAX(time_deviation)`
- **Unit**: Days
- **Interpretation**: Peak schedule variance
- **Python**:
  ```python
  time_deviation_max = df.groupby(period)['time_deviation'].max()
  ```

#### `schedule_adherence`
- **Name**: Schedule Adherence Score
- **Definition**: Normalized on-time performance (0-100 scale)
- **Formula**: `100 - (|time_deviation_avg| / max_deviation * 100)`
- **Unit**: Score (0-100)
- **Interpretation**:
  - 100 = Perfect on-time
  - 50 = Moderate delays
  - 0 = Maximum delays
- **Target**: ≥ 80
- **Python**:
  ```python
  max_dev = abs(time_deviation_avg).max()
  schedule_adherence = 100 - (abs(time_deviation_avg) / max_dev * 100)
  ```

---

### 🔧 Resource Metrics

#### `utilization_avg`
- **Name**: Average Equipment Utilization
- **Definition**: Mean percentage of equipment actively in use
- **Formula**: `AVG(equipment_utilization_rate) * 100`
- **Unit**: Percentage (0-100%)
- **Interpretation**: Higher is better, indicates efficient resource deployment
- **Target**: ≥ 70%
- **Python**:
  ```python
  utilization_avg = df.groupby(period)['equipment_utilization_rate'].mean()
  ```

#### `worker_intensity`
- **Name**: Worker Intensity
- **Definition**: Average workforce deployment level
- **Formula**: `AVG(worker_count)`
- **Unit**: Number of workers
- **Interpretation**: Staffing level for capacity planning
- **Python**:
  ```python
  worker_intensity = df.groupby(period)['worker_count'].mean()
  ```

#### `energy_intensity`
- **Name**: Energy Intensity
- **Definition**: Energy consumption per worker
- **Formula**: `AVG(energy_consumption / (worker_count + 1))`
- **Unit**: kWh per worker
- **Interpretation**:
  - Sustainability indicator
  - Higher may indicate equipment-intensive work
  - Lower may indicate efficiency or manual work
- **Python**:
  ```python
  energy_intensity = (df['energy_consumption'] / (df['worker_count'] + 1)).groupby(period).mean()
  ```

#### `resource_utilization`
- **Name**: Combined Resource Utilization
- **Definition**: Weighted combination of equipment and workforce efficiency
- **Formula**: `0.6 * equipment_util + 0.4 * normalized_worker_intensity`
- **Unit**: Score (0-100)
- **Interpretation**: Overall resource deployment efficiency
- **Target**: ≥ 75%
- **Python**:
  ```python
  resource_utilization = (
      utilization_avg * 0.6 + 
      (worker_intensity / worker_intensity.max() * 100) * 0.4
  )
  ```

---

### 📈 Progress Metrics

#### `progress_avg`
- **Name**: Average Progress
- **Definition**: Mean task completion percentage
- **Formula**: `AVG(task_progress)`
- **Unit**: Percentage (0-100%)
- **Interpretation**: Current completion status
- **Python**:
  ```python
  progress_avg = df.groupby(period)['task_progress'].mean()
  ```

#### `progress_velocity`
- **Name**: Progress Velocity
- **Definition**: Rate of change in task completion
- **Formula**: `DIFF(AVG(task_progress))`
- **Unit**: Percentage points per period
- **Interpretation**:
  - Positive = Making progress
  - Negative = Regressing
  - Zero = Stagnant
- **Target**: > 0
- **Python**:
  ```python
  progress_velocity = progress_avg.diff()
  ```

#### `progress_pct`
- **Name**: Progress Percentage
- **Definition**: Alias for progress_avg, normalized to 0-100
- **Formula**: `AVG(task_progress)`
- **Unit**: Percentage
- **Python**:
  ```python
  progress_pct = progress_avg
  ```

---

### 🛡️ Safety Metrics

#### `safety_incident_count`
- **Name**: Total Safety Incidents
- **Definition**: Sum of all incidents in the period
- **Formula**: `SUM(safety_incidents)`
- **Unit**: Count
- **Interpretation**: Absolute number of incidents
- **Target**: 0
- **Python**:
  ```python
  safety_incident_count = df.groupby(period)['safety_incidents'].sum()
  ```

#### `safety_incident_rate`
- **Name**: Safety Incident Rate
- **Definition**: Average incidents per time unit
- **Formula**: `AVG(safety_incidents)`
- **Unit**: Incidents per period
- **Interpretation**: Normalized incident frequency
- **Target**: 0
- **Python**:
  ```python
  safety_incident_rate = df.groupby(period)['safety_incidents'].mean()
  ```

---

### 📊 Data Quality Metrics

#### `data_health_score`
- **Name**: Data Health Index
- **Definition**: Composite data quality score (0-100)
- **Formula**: Weighted average of 4 components:
  - **Completeness (40%)**: `(1 - missing_ratio) * 100`
  - **Outlier Freedom (30%)**: `(1 - outlier_ratio) * 100`
  - **Temporal Continuity (15%)**: `(1 - gap_ratio) * 100`
  - **Validity (15%)**: `(1 - improbable_ratio) * 100`
- **Unit**: Score (0-100)
- **Interpretation**:
  - ≥ 95: Excellent data quality
  - 85-94: Good quality
  - 70-84: Acceptable
  - < 70: Poor quality, review needed
- **Target**: ≥ 95%
- **Python**:
  ```python
  from kpis.etl_kpis import calculate_data_health
  health_score = calculate_data_health(df)
  ```

---

## Aggregation Periods

KPIs can be computed at different time granularities:

### Daily (`freq='D'`)
- **Use case**: Operational monitoring, daily stand-ups
- **Data points**: All metrics aggregated per calendar day
- **Sample size**: Typically 100-1000 raw records per day

### Weekly (`freq='W'`)
- **Use case**: Management reporting, weekly reviews
- **Data points**: All metrics aggregated per calendar week (Mon-Sun)
- **Sample size**: Typically 700-7000 raw records per week

---

## Success Metrics

### Data Health Threshold
- **Target**: ≥ 95% of periods pass data health checks
- **Action**: If < 95%, investigate data pipeline issues

### KPI Reproducibility
- **Requirement**: `compute_project_kpis(df)` must produce identical results for same input
- **Test**: Hash comparison of output DataFrames

### Performance
- **Requirement**: `compute_project_kpis()` completes in < 2 seconds for 50K records
- **Test**: Timed execution

---

## Usage Examples

### Basic Usage

```python
from kpis.etl_kpis import compute_project_kpis
import pandas as pd

# Load data
df = pd.read_csv('construction_project_dataset.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Compute weekly KPIs
weekly_kpis = compute_project_kpis(df, freq='W')

# View latest metrics
print(weekly_kpis.tail(1))
```

### Filter by Data Quality

```python
# Get only high-quality periods
high_quality = weekly_kpis[weekly_kpis['data_health_score'] >= 95]

# Alert on poor quality
poor_quality = weekly_kpis[weekly_kpis['data_health_score'] < 70]
if len(poor_quality) > 0:
    print(f"⚠️ Warning: {len(poor_quality)} periods have poor data quality")
```

### Trend Analysis

```python
import matplotlib.pyplot as plt

# Plot progress velocity over time
plt.figure(figsize=(12, 6))
plt.plot(weekly_kpis['timestamp'], weekly_kpis['progress_velocity'])
plt.title('Project Progress Velocity')
plt.xlabel('Week')
plt.ylabel('Progress Change (%)')
plt.axhline(y=0, color='r', linestyle='--')
plt.show()
```

### Alert on Anomalies

```python
# Cost overrun alert
cost_alert = weekly_kpis[weekly_kpis['cost_efficiency'] < 70]
if len(cost_alert) > 0:
    print(f"🚨 Cost Alert: {len(cost_alert)} weeks with efficiency < 70%")

# Schedule delay alert
schedule_alert = weekly_kpis[weekly_kpis['schedule_adherence'] < 80]
if len(schedule_alert) > 0:
    print(f"⏰ Schedule Alert: {len(schedule_alert)} weeks behind target")
```

---

## KPI Definitions API

```python
from kpis.etl_kpis import get_kpi_definitions

# Get all definitions
definitions = get_kpi_definitions()

# Print specific KPI info
print(definitions['cost_efficiency']['definition'])
print(definitions['cost_efficiency']['formula'])
print(definitions['cost_efficiency']['interpretation'])
```

---

## Notes

1. **Missing Data Handling**: KPIs gracefully handle missing columns by skipping those calculations
2. **Division by Zero**: Worker-based metrics add +1 to denominator to avoid errors
3. **Normalization**: Derived scores (efficiency, adherence) use max values for normalization
4. **Outliers**: Defined as values > 3 IQR from quartiles
5. **Timestamps**: Must be provided in sortable datetime format

---

**Last Updated**: January 10, 2026  
**Version**: 1.0  
**Maintainer**: Team LogPilot

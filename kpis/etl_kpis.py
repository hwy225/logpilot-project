import pandas as pd
import numpy as np

def auto_reconcile_data(df):
    """
    Auto-reconciliation rules (e.g., unit normalization, sensor sanity).
    """
    # unit normalization
    # Normalize energy units to kWh
    if 'energy_consumption' in df.columns:
        df['energy_consumption'] = df['energy_consumption'].apply(
            lambda x: x * 1000 if x < 50 else x  # Assume values < 50 are MWh -> convert to kWh
        )

    # sensor sanity
    sanity_rules = {
        'temperature': (-30, 80),
        'humidity': (0, 100)
    }
    for col, (min_v, max_v) in sanity_rules.items():
        if col in df.columns:
            df[col] = df[col].clip(lower=min_v, upper=max_v)

    return df


def compute_project_kpis(df, freq='W'):
    """
    Compute weekly/daily KPI roll-ups and Data Health Index.
    freq: 'D' for daily, 'W' for weekly
    """
    df = df.copy()
    df = auto_reconcile_data(df)

    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.sort_values('timestamp')

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

    # ---- KPI Roll-ups ----
    df = df.reset_index()
    rollups = df.resample(freq, on='timestamp').agg({
        'cost_deviation': 'mean',
        'time_deviation': 'mean',
        # utilization
        'equipment_utilization_rate': 'mean',
        # energy/worker intensity
        'energy_consumption': 'mean',
        'worker_count': 'mean',
        # task_progress velocity
        'task_progress': ['first', 'last'],
        'safety_incidents': 'sum'
    })
    rollups.columns = ['_'.join(col).strip() for col in rollups.columns.values]
    rollups['progress_velocity'] = rollups['task_progress_last'] - rollups['task_progress_first']
    rollups['worker_intensity'] = rollups['energy_consumption_mean'] / (rollups['worker_count_mean'] + 1e-6)
    rollups['data_health_index'] = data_health_index

    df = df.reset_index()
    rollups_max = df.resample(freq, on='timestamp').agg({
        'cost_deviation': 'max',
        'time_deviation': 'max'
    })
    rollups_max.columns = [f'{col}_max' for col in rollups_max.columns]

    rollups = pd.concat([rollups,rollups_max],axis=1)

    return rollups.reset_index()

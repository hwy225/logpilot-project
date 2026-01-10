"""
KPI ETL Module for Construction Project Analytics
==================================================

Transforms raw construction logs into project-level KPIs with data quality validation.

Functions:
- compute_project_kpis(df, freq='W'): Main aggregation function
- calculate_data_health(df): Data quality scoring
- get_kpi_definitions(): KPI dictionary

Author: Team LogPilot
Date: January 2026
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


def calculate_data_health(df: pd.DataFrame) -> float:
    """
    Calculate data health index based on:
    - Missingness (% complete data)
    - Outliers (values within reasonable ranges)
    - Timestamp gaps
    - Improbable values
    
    Returns: Health score 0-100
    """
    health_scores = []
    
    # 1. Missingness score (40% weight)
    total_cells = df.size
    missing_cells = df.isnull().sum().sum()
    missingness_score = ((total_cells - missing_cells) / total_cells) * 100
    health_scores.append(('missingness', missingness_score, 0.40))
    
    # 2. Outlier detection (30% weight)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outlier_ratios = []
    
    for col in numeric_cols:
        if col in df.columns and df[col].notna().sum() > 0:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 3 * IQR
            upper_bound = Q3 + 3 * IQR
            
            outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            outlier_ratio = outliers / len(df)
            outlier_ratios.append(outlier_ratio)
    
    avg_outlier_ratio = np.mean(outlier_ratios) if outlier_ratios else 0
    outlier_score = (1 - avg_outlier_ratio) * 100
    health_scores.append(('outliers', outlier_score, 0.30))
    
    # 3. Timestamp gaps (15% weight)
    if 'timestamp' in df.columns:
        df_sorted = df.sort_values('timestamp')
        time_diffs = df_sorted['timestamp'].diff()
        median_diff = time_diffs.median()
        
        # Check for gaps > 2x median
        large_gaps = (time_diffs > median_diff * 2).sum()
        gap_ratio = large_gaps / len(df)
        gap_score = (1 - gap_ratio) * 100
    else:
        gap_score = 100  # No timestamp, assume OK
    
    health_scores.append(('timestamp_gaps', gap_score, 0.15))
    
    # 4. Improbable values (15% weight)
    improbable_count = 0
    checks = 0
    
    # Check temperature range
    if 'temperature' in df.columns:
        improbable_count += ((df['temperature'] < -50) | (df['temperature'] > 60)).sum()
        checks += len(df)
    
    # Check humidity range
    if 'humidity' in df.columns:
        improbable_count += ((df['humidity'] < 0) | (df['humidity'] > 100)).sum()
        checks += len(df)
    
    # Check progress range
    if 'task_progress' in df.columns:
        improbable_count += ((df['task_progress'] < 0) | (df['task_progress'] > 100)).sum()
        checks += len(df)
    
    if checks > 0:
        improbable_ratio = improbable_count / checks
        improbable_score = (1 - improbable_ratio) * 100
    else:
        improbable_score = 100
    
    health_scores.append(('improbable_values', improbable_score, 0.15))
    
    # Calculate weighted average
    total_health = sum(score * weight for _, score, weight in health_scores)
    
    return total_health


def compute_project_kpis(df: pd.DataFrame, freq: str = 'W') -> pd.DataFrame:
    """
    Compute project-level KPIs with daily/weekly roll-ups.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw construction project data
    freq : str
        Aggregation frequency: 'D' (daily) or 'W' (weekly)
    
    Returns:
    --------
    pd.DataFrame with aggregated KPIs
    
    KPIs computed:
    - cost_deviation_avg: Average cost deviation
    - cost_deviation_max: Maximum cost deviation
    - time_deviation_avg: Average time deviation
    - time_deviation_max: Maximum time deviation
    - utilization_avg: Average equipment utilization
    - energy_intensity: Energy per worker
    - progress_velocity: Task progress rate
    - worker_intensity: Workers per unit time
    - safety_incident_rate: Incidents per period
    - data_health_score: Data quality index
    """
    
    # Ensure timestamp column
    if 'timestamp' not in df.columns:
        raise ValueError("DataFrame must have 'timestamp' column")
    
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    # Set timestamp as index for resampling
    df.set_index('timestamp', inplace=True)
    
    # Initialize aggregation dictionary
    agg_dict = {}
    
    # Cost deviation KPIs (using Weiyun's naming convention)
    if 'cost_deviation' in df.columns:
        agg_dict['cost_deviation_mean'] = ('cost_deviation', 'mean')
        agg_dict['cost_deviation_max'] = ('cost_deviation', 'max')
    
    # Time deviation KPIs (using Weiyun's naming convention)
    if 'time_deviation' in df.columns:
        agg_dict['time_deviation_mean'] = ('time_deviation', 'mean')
        agg_dict['time_deviation_max'] = ('time_deviation', 'max')
    
    # Equipment utilization (using Weiyun's naming convention)
    if 'equipment_utilization_rate' in df.columns:
        agg_dict['equipment_utilization_rate_mean'] = ('equipment_utilization_rate', 'mean')
        agg_dict['equipment_utilization_rate_max'] = ('equipment_utilization_rate', 'max')
    
    # Energy intensity (energy per worker)
    if 'energy_consumption' in df.columns and 'worker_count' in df.columns:
        df['energy_per_worker'] = df['energy_consumption'] / (df['worker_count'] + 1)  # +1 to avoid div by 0
        agg_dict['energy_intensity'] = ('energy_per_worker', 'mean')
    
    # Worker intensity
    if 'worker_count' in df.columns:
        agg_dict['worker_intensity'] = ('worker_count', 'mean')
    
    # Safety incidents
    if 'safety_incidents' in df.columns:
        agg_dict['safety_incident_count'] = ('safety_incidents', 'sum')
        agg_dict['safety_incident_rate'] = ('safety_incidents', 'mean')
    
    # Progress velocity (using Weiyun's naming convention)
    if 'task_progress' in df.columns:
        agg_dict['task_progress_first'] = ('task_progress', 'first')
        agg_dict['task_progress_last'] = ('task_progress', 'last')
        agg_dict['task_progress_mean'] = ('task_progress', 'mean')
    
    # Material usage
    if 'material_usage' in df.columns:
        agg_dict['material_usage_avg'] = ('material_usage', 'mean')
    
    # Risk score
    if 'risk_score' in df.columns:
        agg_dict['risk_score_avg'] = ('risk_score', 'mean')
        agg_dict['risk_score_max'] = ('risk_score', 'max')
    
    # Perform aggregation
    kpi_df = df.resample(freq).agg(**agg_dict)
    
    # Calculate progress velocity (change in progress) - Weiyun's method
    if 'task_progress_last' in kpi_df.columns and 'task_progress_first' in kpi_df.columns:
        kpi_df['progress_velocity'] = kpi_df['task_progress_last'] - kpi_df['task_progress_first']
    
    # Calculate data health score for each period
    health_scores = []
    for period_start in kpi_df.index:
        if freq == 'W':
            period_end = period_start + pd.Timedelta(days=7)
        else:  # Daily
            period_end = period_start + pd.Timedelta(days=1)
        
        period_data = df[period_start:period_end]
        if len(period_data) > 0:
            health = calculate_data_health(period_data)
            health_scores.append(health)
        else:
            health_scores.append(np.nan)
    
    # Use Weiyun's naming: data_health_index (not data_health_score)
    kpi_df['data_health_index'] = health_scores
    
    # Add derived KPIs
    # Resource utilization (combination of equipment and workers)
    if 'equipment_utilization_rate_mean' in kpi_df.columns and 'worker_intensity' in kpi_df.columns:
        kpi_df['resource_utilization'] = (
            kpi_df['equipment_utilization_rate_mean'] * 0.6 + 
            (kpi_df['worker_intensity'] / kpi_df['worker_intensity'].max() * 100) * 0.4
        )
    elif 'equipment_utilization_rate_mean' in kpi_df.columns:
        kpi_df['resource_utilization'] = kpi_df['equipment_utilization_rate_mean']
    
    # Cost efficiency (inverse of cost deviation, normalized)
    if 'cost_deviation_mean' in kpi_df.columns:
        # Lower deviation = higher efficiency
        max_dev = abs(kpi_df['cost_deviation_mean']).max()
        if max_dev > 0:
            kpi_df['cost_efficiency'] = 100 - (abs(kpi_df['cost_deviation_mean']) / max_dev * 100)
        else:
            kpi_df['cost_efficiency'] = 100
    
    # Schedule adherence (inverse of time deviation)
    if 'time_deviation_mean' in kpi_df.columns:
        max_dev = abs(kpi_df['time_deviation_mean']).max()
        if max_dev > 0:
            kpi_df['schedule_adherence'] = 100 - (abs(kpi_df['time_deviation_mean']) / max_dev * 100)
        else:
            kpi_df['schedule_adherence'] = 100
    
    # Progress percentage (normalize to 0-100) - use last progress
    if 'task_progress_last' in kpi_df.columns:
        kpi_df['progress_pct'] = kpi_df['task_progress_last']
    
    # Fill NaN values with 0 for new rows
    kpi_df = kpi_df.fillna(0)
    
    # Reset index to make timestamp a column
    kpi_df = kpi_df.reset_index()
    
    return kpi_df


def get_kpi_definitions() -> Dict[str, Dict[str, str]]:
    """
    Get KPI dictionary with definitions and calculation methods.
    Matches Weiyun's original column naming conventions.
    
    Returns:
    --------
    Dict with KPI name as key and definition/formula as value
    """
    
    return {
        'cost_deviation_mean': {
            'name': 'Average Cost Deviation',
            'definition': 'Mean deviation from budgeted costs over the period',
            'formula': 'AVG(cost_deviation)',
            'unit': 'currency',
            'interpretation': 'Positive = over budget, Negative = under budget'
        },
        'cost_deviation_max': {
            'name': 'Maximum Cost Deviation',
            'definition': 'Largest cost deviation observed in the period',
            'formula': 'MAX(cost_deviation)',
            'unit': 'currency',
            'interpretation': 'Peak budget variance'
        },
        'time_deviation_mean': {
            'name': 'Average Time Deviation',
            'definition': 'Mean deviation from scheduled timeline',
            'formula': 'AVG(time_deviation)',
            'unit': 'days',
            'interpretation': 'Positive = ahead, Negative = behind schedule'
        },
        'time_deviation_max': {
            'name': 'Maximum Time Deviation',
            'definition': 'Largest time deviation in the period',
            'formula': 'MAX(time_deviation)',
            'unit': 'days',
            'interpretation': 'Peak schedule variance'
        },
        'equipment_utilization_rate_mean': {
            'name': 'Average Equipment Utilization',
            'definition': 'Mean percentage of equipment actively in use',
            'formula': 'AVG(equipment_utilization_rate)',
            'unit': '%',
            'interpretation': 'Higher is better, indicates efficient resource use'
        },
        'energy_intensity': {
            'name': 'Energy Intensity',
            'definition': 'Average energy consumption per worker',
            'formula': 'AVG(energy_consumption / worker_count)',
            'unit': 'kWh per worker',
            'interpretation': 'Lower may indicate efficiency, higher may indicate intensive work'
        },
        'worker_intensity': {
            'name': 'Worker Intensity',
            'definition': 'Average number of workers on site',
            'formula': 'AVG(worker_count)',
            'unit': 'workers',
            'interpretation': 'Workforce deployment level'
        },
        'safety_incident_rate': {
            'name': 'Safety Incident Rate',
            'definition': 'Average incidents per time period',
            'formula': 'AVG(safety_incidents)',
            'unit': 'incidents per period',
            'interpretation': 'Lower is better, target is 0'
        },
        'progress_velocity': {
            'name': 'Progress Velocity',
            'definition': 'Rate of change in task completion',
            'formula': 'task_progress_last - task_progress_first',
            'unit': '% per period',
            'interpretation': 'Positive = progressing, Negative = regressing'
        },
        'task_progress_last': {
            'name': 'Task Progress',
            'definition': 'Latest task completion percentage in period',
            'formula': 'LAST(task_progress)',
            'unit': '%',
            'interpretation': 'Project completion status'
        },
        'data_health_index': {
            'name': 'Data Health Index',
            'definition': 'Composite data quality score (0-100)',
            'formula': 'Weighted avg: Completeness(40%) + Outliers(30%) + Gaps(15%) + Validity(15%)',
            'unit': 'score (0-100)',
            'interpretation': 'Higher is better, target ≥95%'
        },
        'resource_utilization': {
            'name': 'Resource Utilization',
            'definition': 'Combined equipment and workforce utilization',
            'formula': '0.6 * equipment_util + 0.4 * normalized_worker_intensity',
            'unit': '%',
            'interpretation': 'Overall resource efficiency'
        },
        'cost_efficiency': {
            'name': 'Cost Efficiency',
            'definition': 'Inverse of cost deviation (higher = more efficient)',
            'formula': '100 - (|cost_deviation| / max_deviation * 100)',
            'unit': 'score (0-100)',
            'interpretation': 'Higher is better, 100 = perfect adherence'
        },
        'schedule_adherence': {
            'name': 'Schedule Adherence',
            'definition': 'Inverse of time deviation (higher = better on-time)',
            'formula': '100 - (|time_deviation| / max_deviation * 100)',
            'unit': 'score (0-100)',
            'interpretation': 'Higher is better, 100 = perfect on-time'
        },
        'progress_pct': {
            'name': 'Progress Percentage',
            'definition': 'Average task completion percentage',
            'formula': 'AVG(task_progress)',
            'unit': '%',
            'interpretation': 'Project completion status'
        }
    }


# Test function
if __name__ == "__main__":
    # Example usage
    print("KPI ETL Module - Test")
    print("=" * 50)
    
    # Load sample data
    df = pd.read_csv("../data/construction_project_dataset.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Compute weekly KPIs
    print("\nComputing Weekly KPIs...")
    weekly_kpis = compute_project_kpis(df, freq='W')
    print(f"✅ Generated {len(weekly_kpis)} weekly periods")
    print(f"   Columns: {list(weekly_kpis.columns)}")
    print(f"\n   Latest period metrics:")
    print(weekly_kpis.tail(1).T)
    
    # Compute daily KPIs
    print("\n\nComputing Daily KPIs...")
    daily_kpis = compute_project_kpis(df.head(10000), freq='D')  # Use subset for speed
    print(f"✅ Generated {len(daily_kpis)} daily periods")
    
    # Show KPI definitions
    print("\n\nKPI Definitions:")
    definitions = get_kpi_definitions()
    for kpi_name, details in list(definitions.items())[:3]:
        print(f"\n{kpi_name}:")
        print(f"  {details['definition']}")
        print(f"  Formula: {details['formula']}")

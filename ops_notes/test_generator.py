"""
Test/Demo Script for Weekly Ops Notes Generator
================================================
Generates a sample weekly report using real data preparation.

This script:
1. Loads actual construction project data
2. Prepares features for time overrun predictions
3. Creates safety monitoring data
4. Generates weekly ops notes

Usage:
    1. Add GEMINI_API_KEY to .env file
    2. Run: python ops_notes/test_generator.py
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent.parent))

from ops_notes.generator import WeeklyOpsNotesGenerator


def load_project_data():
    """
    Load and prepare project data for time overrun predictions.
    Creates sample projects with required LAG features.
    """
    print("\n📊 Preparing sample project data...")
    
    # Load dataset to get realistic feature ranges
    data_path = Path(__file__).parent.parent / 'data' / 'construction_project_dataset.csv'
    df = pd.read_csv(data_path)
    
    print(f"✅ Loaded {len(df)} records from dataset")
    
    # Get required features from the model
    # Based on the error, we need lag features (lag2, lag5)
    base_features = [
        'temperature', 'humidity', 'vibration_level', 'material_usage',
        'machinery_status', 'worker_count', 'energy_consumption', 'task_progress',
        'cost_deviation', 'time_deviation', 'safety_incidents',
        'equipment_utilization_rate', 'material_shortage_alert', 'risk_score'
    ]
    
    # Create lag features
    lag_features = []
    for lag in [2, 5]:
        for col in base_features:
            if col in df.columns:
                df[f'{col}_lag{lag}'] = df[col].shift(lag)
                lag_features.append(f'{col}_lag{lag}')
    
    # Fill NaN values with mean
    df = df.fillna(df.mean(numeric_only=True))
    
    print(f"✅ Created {len(lag_features)} lag features")
    
    # Create sample projects
    np.random.seed(42)
    projects_data = []
    project_names = ['Alpha_Tower', 'Beta_Bridge', 'Gamma_Complex', 'Delta_Plaza', 'Echo_Center']
    
    for i, project_name in enumerate(project_names):
        # Sample a slice of data to represent this "project"
        start_idx = i * 1000
        end_idx = min((i + 1) * 1000, len(df))
        sample_slice = df.iloc[start_idx:end_idx] if len(df) > 1000 else df.sample(min(100, len(df)))
        
        # Extract features - use mean values as project characteristics
        features = {}
        all_feature_cols = base_features + lag_features
        
        for col in all_feature_cols:
            if col in sample_slice.columns:
                features[col] = float(sample_slice[col].mean())
        
        projects_data.append({
            'project_id': project_name,
            'features': features
        })
    
    print(f"✅ Created {len(projects_data)} sample projects")
    print(f"Each project has {len(projects_data[0]['features'])} features")
    return projects_data


def create_sample_safety_data(week_start: str, week_end: str):
    """
    Create sample safety monitoring data for the week.
    In production, this would come from sensors/daily reports.
    """
    print(f"\n🛡️ Creating safety data for {week_start} to {week_end}...")
    
    # Generate dates
    dates = pd.date_range(week_start, week_end, freq='D')
    
    # Create realistic sample data
    np.random.seed(42)  # For reproducibility
    
    safety_data = pd.DataFrame({
        'date': dates,
        'vibration_level': np.random.uniform(20, 30, len(dates)),  # Some days might exceed 25.16 threshold
        'temperature': np.random.uniform(26, 34, len(dates)),       # Some days might exceed 30°C threshold
        'humidity': np.random.uniform(60, 80, len(dates)),
        'worker_count': np.random.randint(40, 60, len(dates)),      # Match safety API column name
        'equipment_count': np.random.randint(7, 12, len(dates))
    })
    
    # Introduce a high-risk day (Tuesday)
    if len(safety_data) >= 2:
        safety_data.loc[1, 'vibration_level'] = 28.5  # Exceeds threshold
        safety_data.loc[1, 'temperature'] = 33         # Exceeds threshold
        safety_data.loc[1, 'worker_count'] = 58        # Fixed column name
        safety_data.loc[1, 'equipment_count'] = 11
    
    print(f"✅ Created {len(safety_data)} days of safety data")
    print("\nSample data:")
    print(safety_data.head())
    
    return safety_data


def main():
    """
    Main test/demo function.
    """
    print("=" * 80)
    print("WEEKLY OPS NOTES GENERATOR - TEST/DEMO")
    print("=" * 80)
    
    # Check API key
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("\n❌ ERROR: GEMINI_API_KEY not found")
        print("\nPlease add it to your .env file:")
        print("  1. Create/edit .env file in project root")
        print("  2. Add this line: GEMINI_API_KEY=your-api-key-here")
        print("\nTo get a key:")
        print("  1. Go to https://makersuite.google.com/app/apikey")
        print("  2. Create a new API key")
        print("  3. Copy and paste into .env file")
        print("\nAlternatively, set as environment variable:")
        print("  export GEMINI_API_KEY='your-api-key'")
        return
        return
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    # Define week to analyze
    week_start = '2026-01-06'
    week_end = '2026-01-10'
    
    try:
        # Load project data
        projects_data = load_project_data()
        
        # Create safety data
        safety_data = create_sample_safety_data(week_start, week_end)
        
        # Initialize generator
        print("\n🤖 Initializing generator...")
        generator = WeeklyOpsNotesGenerator(gemini_api_key=api_key)
        
        # Generate report
        output_path = f'ops_notes/samples/week_{week_start}.md'
        report = generator.generate_weekly_report(
            projects_data=projects_data,
            safety_data=safety_data,
            week_start=week_start,
            week_end=week_end,
            output_path=output_path
        )
        
        # Print preview
        print("\n" + "=" * 80)
        print("REPORT PREVIEW (First 1000 characters):")
        print("=" * 80)
        print(report[:1000])
        print("\n[... rest of report ...]")
        print("\n" + "=" * 80)
        print(f"✅ Full report saved to: {output_path}")
        print("=" * 80)
        
        # Success metrics
        print("\n📊 SUCCESS METRICS:")
        print(f"  - Report length: {len(report)} characters")
        print(f"  - Contains Executive Summary: {'Executive Summary' in report}")
        print(f"  - Contains Recommendations: {'Recommended Actions' in report or 'Recommendation' in report}")
        print(f"  - Contains Raw Data: {'Raw Data' in report}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n✅ TEST COMPLETE!")


if __name__ == "__main__":
    main()

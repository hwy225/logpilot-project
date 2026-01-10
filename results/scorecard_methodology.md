# Project Scorecard Methodology

## Overview
Composite Performance Score combining 5 normalized pillars (0-100 scale).

## Pillars & Weights

- **Schedule**: 0.013 (1.3%)
- **Cost**: 0.045 (4.5%)
- **Utilization**: 0.023 (2.3%)
- **Safety**: 0.897 (89.7%)
- **Risk**: 0.023 (2.3%)

## Scoring Formula

Composite_Score = Σ (Pillar_i × Weight_i)

## Normalization Method
MinMaxScaler: (X - X_min) / (X_max - X_min) × 100

## Traffic Light Categories
- 🟢 Excellent: 80-100
- 🟡 Good: 65-79
- 🟠 Fair: 50-64
- 🔴 Poor: 35-49
- ⚫ Critical: 0-34

## Validation Results

- Correlation with existing Performance_Score: nan
- R² Score: 0.0000
- Mean Absolute Error: 3.06
- Target correlation (≥0.6):  NOT MET

## Stability Metrics
- Mean weekly variance: 88.08
- Week-over-week stability:  STABLE

## Generated: 2026-01-09 17:36:28

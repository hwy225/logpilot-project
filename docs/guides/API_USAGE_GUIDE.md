# Overrun Watch API - Usage Guide

## 🚀 Quick Start

```python
from models.overrun_api import OverrunPredictor

# Initialize predictor (loads all models automatically)
# The API automatically finds models whether you run from project root or models/ directory
predictor = OverrunPredictor()  # Uses default: 'saved_models'
# Or explicitly specify: predictor = OverrunPredictor(model_dir='models/saved_models')
```

## 📊 Core Features

### 1. Single Project Prediction

#### TIME Overrun (Production Model - 100% Precision@1)
```python
# Prepare features (LAG-only features for TIME)
project_features = {
    'safety_incidents_lag1': 0.5,
    'material_shortage_alert_lag2': 1.0,
    # ... other TIME features
}

# Get prediction
result = predictor.predict_time_overrun(
    X=project_features,
    project_id="Project_Alpha"
)

print(f"Prediction: {result['prediction_label']}")
print(f"Confidence: {result['confidence_pct']}")
print(f"Recommendation: {result['recommendation']}")
```

**Output:**
```
Prediction: OVERRUN
Confidence: 87.5%
Recommendation: 🚨 HIGH RISK - Immediate review required (100% Precision@1)
```

#### COST Overrun (Experimental Model - Directional)
```python
result = predictor.predict_cost_overrun(
    X=project_features,  # Derived + LAG features for COST
    project_id="Project_Alpha"
)
```

### 2. Batch Project Ranking

**Most Useful for Weekly Reviews!**

```python
# Prepare list of projects
projects = [
    {
        'project_id': 'Alpha',
        'features': alpha_features_df
    },
    {
        'project_id': 'Beta', 
        'features': beta_features_df
    },
    {
        'project_id': 'Gamma',
        'features': gamma_features_df
    }
]

# Rank by TIME overrun risk, show top 3
top_risks = predictor.rank_projects(
    projects=projects,
    target='time',
    top_k=3
)

print(top_risks)
```

**Output:**
```
 rank project_id  confidence confidence_pct prediction                      recommendation
    1       Alpha    0.875000          87.5%    OVERRUN 🚨 HIGH RISK - Immediate review required
    2        Beta    0.653000          65.3%    OVERRUN ⚠️  MEDIUM RISK - Schedule review this week
    3       Gamma    0.420000          42.0% NO_OVERRUN ✅ Low risk - Continue monitoring
```

### 3. Combined Prediction (TIME + COST)

```python
result = predictor.predict_both(
    X_time=time_features,
    X_cost=cost_features,
    project_id="Project_Alpha"
)

print(f"TIME: {result['time_overrun']['prediction_label']} ({result['time_overrun']['confidence_pct']})")
print(f"COST: {result['cost_overrun']['prediction_label']} ({result['cost_overrun']['confidence_pct']})")
print(f"Overall Risk: {result['overall_risk_level']}")
```

### 4. Generate Alerts

```python
# Get prediction
result = predictor.predict_time_overrun(features, project_id="Alpha")

# Generate alert in different formats
text_alert = predictor.generate_alert(result, format='text')
markdown_alert = predictor.generate_alert(result, format='markdown')
html_alert = predictor.generate_alert(result, format='html')

# Send via email, Slack, dashboard, etc.
send_email(to="pm@company.com", body=text_alert)
```

**Sample Alert:**
```
============================================================
OVERRUN WATCH ALERT
============================================================
Project: Alpha
Target: TIME_OVERRUN
Prediction: OVERRUN
Confidence: 87.5%
Model Status: PRODUCTION

Recommendation:
  🚨 HIGH RISK - Immediate review required (100% Precision@1)
============================================================
```

### 5. Feature Importance (Explainability)

```python
# Get top drivers for TIME overruns
importance = predictor.get_feature_importance('time', top_n=10)
print(importance)
```

**Output:**
```
                         feature  importance
0             safety_incidents    0.8186
1       safety_incidents_lag2    0.5955
2  material_shortage_alert_lag5  0.4105
3  material_shortage_alert_lag2  0.2407
4       safety_incidents_lag5    0.1938
```

## 🎯 Real-World Workflows

### Workflow 1: Daily Automated Alerts

```python
import schedule
import time

def daily_risk_check():
    """Run daily at 8 AM to check all active projects."""
    
    # Load today's project data
    active_projects = load_active_projects()
    
    # Rank all projects
    ranked = predictor.rank_projects(
        projects=active_projects,
        target='time',
        top_k=3
    )
    
    # Send alerts for top 3 highest-risk
    for _, project in ranked.iterrows():
        if project['confidence'] > 0.6:  # Only alert if >60% confidence
            features = get_project_features(project['project_id'])
            result = predictor.predict_time_overrun(features, project['project_id'])
            alert = predictor.generate_alert(result, format='markdown')
            
            # Send to project manager
            send_slack_message(
                channel='#project-alerts',
                message=alert
            )

# Schedule daily at 8 AM
schedule.every().day.at("08:00").do(daily_risk_check)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Workflow 2: On-Demand Risk Assessment

```python
def check_project_risk(project_id: str):
    """Check risk for a specific project on-demand."""
    
    # Get latest features
    features_time = get_latest_features(project_id, feature_set='time')
    features_cost = get_latest_features(project_id, feature_set='cost')
    
    # Get predictions
    result = predictor.predict_both(
        X_time=features_time,
        X_cost=features_cost,
        project_id=project_id
    )
    
    # Generate comprehensive report
    report = f"""
    PROJECT RISK ASSESSMENT: {project_id}
    =====================================
    
    TIME OVERRUN:
      Status: {result['time_overrun']['prediction_label']}
      Confidence: {result['time_overrun']['confidence_pct']}
      Model: {result['time_overrun']['model_status']}
      → {result['time_overrun']['recommendation']}
    
    COST OVERRUN:
      Status: {result['cost_overrun']['prediction_label']}
      Confidence: {result['cost_overrun']['confidence_pct']}
      Model: {result['cost_overrun']['model_status']}
      → {result['cost_overrun']['recommendation']}
    
    OVERALL RISK LEVEL: {result['overall_risk_level']}
    """
    
    return report

# Usage
report = check_project_risk('Alpha')
print(report)
```

### Workflow 3: Weekly Executive Summary

```python
def weekly_executive_summary():
    """Generate weekly summary for leadership."""
    
    active_projects = load_active_projects()
    
    # Rank all projects by TIME risk
    time_ranked = predictor.rank_projects(active_projects, target='time')
    
    # Count risk levels
    high_risk = time_ranked[time_ranked['confidence'] >= 0.7]
    medium_risk = time_ranked[(time_ranked['confidence'] >= 0.5) & 
                              (time_ranked['confidence'] < 0.7)]
    low_risk = time_ranked[time_ranked['confidence'] < 0.5]
    
    summary = f"""
    WEEKLY PROJECT RISK SUMMARY
    ===========================
    
    Total Active Projects: {len(active_projects)}
    
    Risk Distribution:
      🔴 HIGH RISK: {len(high_risk)} projects (≥70% confidence)
      🟡 MEDIUM RISK: {len(medium_risk)} projects (50-70%)
      🟢 LOW RISK: {len(low_risk)} projects (<50%)
    
    Top 5 Highest Risk Projects:
    {time_ranked.head(5).to_string(index=False)}
    
    Recommended Actions:
      - Immediate review: {len(high_risk)} projects
      - Schedule review this week: {len(medium_risk)} projects
      - Continue monitoring: {len(low_risk)} projects
    """
    
    send_email(
        to="leadership@company.com",
        subject="Weekly Project Risk Summary",
        body=summary
    )

# Run every Monday at 9 AM
schedule.every().monday.at("09:00").do(weekly_executive_summary)
```

## 📋 API Reference

### Class: `OverrunPredictor`

#### Methods:

| Method | Description | Returns |
|--------|-------------|---------|
| `predict_time_overrun(X, project_id)` | Predict TIME overrun for single project | Dict with prediction, confidence, recommendation |
| `predict_cost_overrun(X, project_id)` | Predict COST overrun for single project | Dict with prediction, confidence, recommendation |
| `predict_both(X_time, X_cost, project_id)` | Predict both TIME and COST | Combined dict with both results |
| `rank_projects(projects, target, top_k)` | Rank multiple projects by risk | DataFrame sorted by confidence |
| `get_feature_importance(target, top_n)` | Get top feature drivers | DataFrame with features and importance |
| `generate_alert(result, format)` | Generate formatted alert | String (text/markdown/html) |

### Input Requirements:

#### TIME Model Features (10 LAG features):
- `safety_incidents_lag1` through `lag7`
- `material_shortage_alert_lag1` through `lag7`
- Selected LAG features based on correlation analysis

#### COST Model Features (10 Derived + LAG features):
- Derived KPIs: `material_usage_change`, `vibration_change`, etc.
- LAG features: `risk_score_lag5`, `vibration_level_lag7`, etc.
- Selected features based on mixed strategy

**Note:** Feature names must match exactly what the models were trained on. Check `model_metadata.pkl` for complete list.

## ⚠️ Important Notes

### Model Maturity Levels:

| Model | Status | AUC | Precision@1 | Use Case |
|-------|--------|-----|-------------|----------|
| **TIME** | **PRODUCTION** | **0.750** | **100%** | **Use for operational decisions** |
| **COST** | **EXPERIMENTAL** | **0.444** | **N/A** | **Use for directional guidance only** |

### Best Practices:

1. **Trust TIME predictions for operational use** - especially top-1 and top-2 alerts (100% accurate)
2. **Use COST predictions with domain expertise** - treat as signals, not absolute truth
3. **Focus on top-k rankings** - you can't review all projects, prioritize top 3-5
4. **Combine with manager judgment** - AI supports decisions, doesn't replace them
5. **Retrain periodically** - as you collect more data, retrain models to improve

### Error Handling:

```python
try:
    result = predictor.predict_time_overrun(features)
except ValueError as e:
    print(f"Invalid features: {e}")
except RuntimeError as e:
    print(f"Model error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🚀 Next Steps

1. **Integration**: Connect to your project management system's database
2. **Automation**: Set up daily/weekly scheduled predictions
3. **Alerting**: Configure Slack/email notifications for high-risk projects
4. **Dashboard**: Build visualization dashboard showing real-time risk levels
5. **Feedback Loop**: Track model performance and retrain with new data

## 📞 Support

For questions or issues:
- Technical: See `test_api.py` for comprehensive examples
- Models: See `NOTEBOOKS_SUMMARY.md` for training details
- Business: See `ONE_PAGER_PROJECT_MANAGERS.md` for stakeholder overview

---

*Generated: November 17, 2025 | Logpilot Project Team*

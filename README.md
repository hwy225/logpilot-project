# 🏗️ LogPilot: Construction Intelligence Platform

**AI-Powered Analytics & Decision Support for Construction Projects**

*Industry-Academia Collaboration | Masters in Data Science | January 2026*

[![Status](https://img.shields.io/badge/Status-Production%20Ready-green)]()
[![TIME Model](https://img.shields.io/badge/TIME%20AUC-0.750-blue)]()
[![Precision@1](https://img.shields.io/badge/Precision@1-100%25-brightgreen)]()

---

## 📋 Overview

**LogPilot** is a comprehensive ML platform transforming construction telemetry into actionable insights. The system provides real-time KPIs, predictive risk signals, interactive simulations, and automated reporting for construction project management.

### 🎯 Core Capabilities

- **Real-time KPI Monitoring** - Data quality validation + project health metrics
- **Risk Prediction** - AI-powered early warning for time/cost overruns
- **Anomaly Detection** - Drift patterns in utilization and progress
- **What-If Simulation** - Interactive scenario analysis (<300ms response)
- **Safety Monitoring** - Leading indicators for incident prevention
- **Project Scorecard** - Composite performance scoring across pillars
- **Automated Reporting** - LLM-powered weekly operations summaries

---

## 👥 Team Contributions

| Task | Owner | Module | Status |
|------|-------|--------|--------|
| **Task 1** | Weiyun | KPI Dashboard & What-If Simulation | ✅ Complete |
| **Task 2** | Vyoma | Time/Cost Overrun Prediction | ✅ Complete |
| **Task 3** | Feruz | Utilization & Progress Drift Detection | ✅ Complete |
| **Task 4** | Weiyun | What-If Micro-Simulation (Core) | ✅ Complete |
| **Task 5** | Vyoma | Safety Signal Board | ✅ Complete |
| **Task 6** | Feruz | Project Scorecard | ✅ Complete |
| **Task 7** | Vyoma | Weekly Ops Notes (LLM) | ✅ Complete |

---

## 📦 Module Summaries

### 🎯 Task 1: KPI Dashboard (Weiyun)
**Location:** `kpis/`, `app_kpis.py`

Real-time project KPI computation with data quality validation:
- Daily/weekly aggregation
- KPI dictionary with formal definitions
- Data health checks and anomaly flagging
- Interactive Streamlit dashboard

**Run:**
```bash
streamlit run app_kpis.py
```

---

### ⚠️ Task 2: Overrun Watch (Vyoma)
**Location:** `models/`

Early-warning system for TIME and COST overruns:
- **TIME Model:** 0.750 AUC, **100% Precision@1** (top alert always correct)
- **COST Model:** 0.444 AUC (experimental, directional guidance)
- Production API for real-time predictions
- Ranks projects by risk for proactive intervention

**Quick Start:**
```bash
# Test API
python test_api.py

# Use in code
from models.overrun_api import OverrunPredictor
predictor = OverrunPredictor()
result = predictor.predict_time_overrun(features, project_id="Alpha")
```

**Documentation:** [models/README.md](models/README.md) | [API Guide](docs/guides/API_USAGE_GUIDE.md)

---

### 🔍 Task 3: Drift Detection (Feruz)
**Location:** `Anomaly_Detection.ipynb`, `results/`

Anomaly detection for operational inefficiencies:
- **Method:** Isolation Forest for progress drift
- Episode detection and tracking
- Alert JSON generation for integration
- Visualizations: progress anomalies, drift episodes

**Outputs:**
- `results/task3_alerts.json` - Alert data
- `results/task3_drift_episodes.csv` - Episode timeline
- `results/progress_anomaly.png` - Visualization

---

### 🎮 Task 4: What-If Simulation (Weiyun)
**Location:** `sim/`

Interactive scenario analysis for operational decisions:
- **Response Time:** <300ms (real-time user experience)
- **Models:** LightGBM surrogate models (P10, P50, P90)
- **Input:** Crew size, utilization changes
- **Output:** Predicted progress delta with uncertainty
- Streamlit UI for PM-friendly interaction

**Run:**
```bash
streamlit run sim/app.py
```

**Demo:** `sim/ux_mock.mp4`

---

### 🛡️ Task 5: Safety Signal Board (Vyoma)
**Location:** `safety/`

Leading indicators for next-day safety risk (24hr advance warning):
- **Approach:** Rule-based system (beats 9 ML approaches!)
- **Performance:** Recall=1.00 (catches ALL high-risk days), Precision=0.80
- **Thresholds:** Vibration > 25.16, Heat > 30°C, Density > 0.36
- Production API for daily risk assessment

**Quick Start:**
```bash
# Run production notebook
jupyter notebook safety/leading_index.ipynb

# Use API
from safety.safety_dashboard import SafetyAlertSystem
safety = SafetyAlertSystem()
result = safety.predict_daily_risk(date, vibration, temp, humidity, workers, equipment)
```

**Documentation:** [safety/README.md](safety/README.md) | [HSE Report](docs/deliverables/TASK5_HSE_SAFETY_REPORT.md)

---

### 📊 Task 6: Project Scorecard (Feruz)
**Location:** `Project_Scorecard.ipynb`, `results/`

Composite performance scoring across multiple pillars:
- Aggregates project health metrics
- Daily per-site exports
- Interactive HTML dashboards (radar charts, distributions)
- Weekly scorecard summaries

**Outputs:**
- `results/scorecard_dashboard.html` - Interactive visualization
- `results/daily_scorecard_per_site.csv` - Daily metrics
- `results/weekly_scorecard_summary.csv` - Weekly rollup
- `results/pillar_radar.html` - Pillar performance radar
- `results/scorecard_methodology.md` - Methodology documentation

---

### 📝 Task 7: Weekly Ops Notes (Vyoma)
**Location:** `ops_notes/`

AI-powered weekly operations summary generator:
- **LLM:** Google Gemini for narrative generation
- **Input:** Time overrun predictions + Safety alerts
- **Output:** Executive summary, risk analysis, action items
- **Target:** <2 minutes PM review time, ≥70% acceptance rate

**Quick Start:**
```bash
# Add API key to .env
echo "GEMINI_API_KEY=your-key" > .env

# Run test
python ops_notes/test_generator.py

# View generated report
cat ops_notes/samples/week_YYYY_MM_DD.md
```

**Documentation:** [ops_notes/README.md](ops_notes/README.md)

---

## 📁 Repository Structure

```
logpilot-project/
│
├── README.md                              # This file
├── requirements.txt                       # Python dependencies
│
├── data/                                  # 📂 Raw datasets
│   ├── construction_project_dataset.csv
│   └── construction_project_performance_dataset.csv
│
├── kpis/                                  # 🎯 Task 1: KPI Dashboard (Weiyun)
│   ├── etl_kpis.py                       # KPI computation engine
│   ├── kpi_dictionary.md                 # Formal KPI definitions
│   └── __init__.py
│
├── models/                                # ⚠️ Task 2: Overrun Prediction (Vyoma)
│   ├── overrun_api.py                    # Production API
│   ├── model_training.ipynb              # Training & evaluation
│   └── saved_models/                     # Trained models (.pkl)
│       ├── time_stacking_model.pkl       # ⭐ Best TIME model
│       └── cost_lr_model.pkl             # COST model
│
├── Anomaly_Detection.ipynb               # 🔍 Task 3: Drift Detection (Feruz)
├── results/                               # Task 3 & 6 outputs
│   ├── task3_alerts.json                 # Anomaly alerts
│   ├── task3_drift_episodes.csv          # Drift timeline
│   ├── scorecard_dashboard.html          # Project scorecard
│   └── ...
│
├── sim/                                   # 🎮 Task 4: What-If Simulation (Weiyun)
│   ├── app.py                            # Streamlit dashboard
│   ├── what_if.py                        # Simulation engine
│   ├── models/                           # Surrogate models (LightGBM)
│   └── experiments/                      # Model training notebooks
│
├── safety/                                # 🛡️ Task 5: Safety Monitoring (Vyoma)
│   ├── safety_dashboard.py               # Production API
│   ├── leading_index.ipynb               # Rule-based system
│   └── saved_safety_models/              # Thresholds & config
│
├── Project_Scorecard.ipynb               # 📊 Task 6: Scorecard (Feruz)
│
├── ops_notes/                             # 📝 Task 7: Ops Notes (Vyoma)
│   ├── generator.py                      # LLM-powered generator
│   ├── test_generator.py                 # Test/demo script
│   ├── prompt.txt                        # LLM prompt template
│   └── samples/                          # Generated reports
│
├── docs/                                  # 📚 Documentation
│   ├── deliverables/                     # Final reports
│   ├── guides/                           # How-to guides
│   └── experiment_logs/                  # Technical details
│
└── app_kpis.py                           # 🎯 Task 1 Dashboard entry point

```

---

## 🚀 Quick Start

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Set up .env file (for Task 7)
echo "GEMINI_API_KEY=your-key-here" > .env
```

### Run Individual Modules

```bash
# Task 1: KPI Dashboard
streamlit run app_kpis.py

# Task 2: Test Overrun Predictor
python test_api.py

# Task 4: What-If Simulation
streamlit run sim/app.py

# Task 5: Safety Analysis
jupyter notebook safety/leading_index.ipynb

# Task 7: Generate Weekly Report
python ops_notes/test_generator.py
```

### View Results & Reports

```bash
# Task 3 & 6: HTML Dashboards
open results/scorecard_dashboard.html
open results/pillar_radar.html

# Task 7: Weekly Reports
cat ops_notes/samples/week_*.md
```

---

## 📊 Key Performance Metrics

| Module | Metric | Performance |
|--------|--------|-------------|
| **Time Overrun (Task 2)** | Precision@1 | **100%** ✅ |
| **Time Overrun (Task 2)** | AUC | 0.750 |
| **Safety (Task 5)** | Recall | **1.00** (catches all high-risk days) ✅ |
| **Safety (Task 5)** | Precision | 0.80 |
| **What-If Sim (Task 4)** | Response Time | <300ms ✅ |
| **Ops Notes (Task 7)** | Review Time | <2 min ✅ |

---

## 🎓 Data Source

**Construction Project Performance Dataset** from Kaggle:
🔗 https://www.kaggle.com/datasets/ziya07/construction-project-performance-dataset

The dataset includes time-series records:
- Project progress and task completion
- Cost and schedule deviations  
- Resource utilization signals
- Environmental and operational metrics

---

## 📖 Documentation

### By Task
- **Task 1:** `kpis/kpi_dictionary.md`
- **Task 2:** `docs/guides/API_USAGE_GUIDE.md`, `docs/deliverables/FINAL_DELIVERABLE_SUMMARY.md`
- **Task 5:** `safety/README.md`, `docs/deliverables/TASK5_HSE_SAFETY_REPORT.md`
- **Task 6:** `results/scorecard_methodology.md`
- **Task 7:** `ops_notes/README.md`

### General Guides
- 📁 [Folder Structure Guide](docs/guides/FOLDER_GUIDE.md)
- 📓 [Notebooks Summary](docs/deliverables/NOTEBOOKS_SUMMARY.md)
- 👔 [One-Pager for PMs](docs/deliverables/ONE_PAGER_PROJECT_MANAGERS.md)

---

## 🔬 Technical Stack

**Core:**
- Python 3.12+
- Pandas, NumPy, Scikit-learn
- XGBoost, LightGBM
- Streamlit (dashboards)

**ML & Analysis:**
- SHAP (interpretability)
- Isolation Forest (anomaly detection)
- Imbalanced-learn (SMOTE)

**LLM Integration:**
- Google Gemini API (Task 7)
- python-dotenv (config management)

---

## 👥 Team & Branches

**Integration Branch:** `team-integration` (this branch)

**Individual Task Branches:**
- `task1_weiyun` - KPI Dashboard & What-If Simulation
- `task2_vyoma` - Time/Cost Overrun + Safety + Ops Notes (Tasks 2, 5, 7)
- `feruz-scorecard` - Project Scorecard (Task 6)
- `feruz-utilization_and_progress_drift` - Anomaly Detection (Task 3)

---

## 🎯 Success Criteria Achieved

✅ **Data Quality:** KPI validation + anomaly detection  
✅ **Predictive Accuracy:** TIME model 100% Precision@1, Safety 100% Recall  
✅ **User Experience:** What-If <300ms, Ops Notes <2min review  
✅ **Production Ready:** APIs, dashboards, automated reporting  
✅ **Documentation:** Comprehensive guides and technical reports  

---

## 🚀 Future Enhancements

- [ ] Unified web dashboard combining all modules
- [ ] Real-time data pipeline integration
- [ ] Mobile app for field operations
- [ ] Multi-project portfolio view
- [ ] Advanced LLM agents for root cause analysis
- [ ] Automated intervention recommendations

---

## 📧 Contact & Support

**Project Team:**
- Weiyun - Task 1, 4 (KPI, Simulation)
- Vyoma - Task 2, 5, 7 (Overrun, Safety, Ops Notes)
- Feruz - Task 3, 6 (Drift Detection, Scorecard)

**Repository:** https://github.com/hwy225/logpilot-project

---

**Last Updated:** January 10, 2026  
**Status:** ✅ All Tasks Complete - Production Ready

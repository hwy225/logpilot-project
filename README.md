# Construction Project Performance & Simulation Platform

This project is an end-to-end **data science, machine learning, and interactive simulation platform** for construction project monitoring and decision support.
It integrates **KPI engineering**, **probabilistic forecasting**, and a **real-time “What-if” simulator**, enabling users to explore operational scenarios with quantified uncertainty.

---

## 🎯 Project Objectives & Success Metrics

This project is designed to meet the following **performance and usability requirements**:

* ⚡ **Low-latency simulation**

  * Scenario response time **< 300 ms**, enabling real-time interaction in the Streamlit UI.
* 📊 **Uncertainty-aware predictions**

  * Probabilistic forecasts with calibrated **prediction intervals** (P10 / P50 / P90).
  * Coverage aligned with quantile definitions (e.g., ~90% coverage for P90).
* 🧑‍💻 **Interactive decision support**

  * Intuitive UI for exploring resource and operational changes.
  * Immediate feedback on projected project progress.

---

## 📦 Deliverables

The project fulfills the required deliverables through the following components:

* **`sim/what_if.py`**
  Core scenario analysis logic that:

  * Applies user-defined changes to the current project state
  * Generates fast, model-based predictions for progress deltas
* **`sim/ux_mock.mp4`**
  Screen-recorded UX demo illustrating:

  * Slider-based scenario adjustments
  * Real-time prediction updates with uncertainty bounds
* **Streamlit-based UI (`sim/app.py`)**

  * Interactive dashboard for scenario exploration
  * Designed for responsiveness and low-latency feedback

---

## 📂 Project Structure

```text
.
├── data/                         # Raw and processed datasets
│   ├── construction_project_*.csv  # Source construction data
│   └── data_preprocessing.ipynb    # Data cleaning & feature engineering
├── kpis/                         # Task 1: KPI Logic & Definitions
│   ├── etl_kpis.py                # ETL scripts for KPI extraction
│   ├── kpi_dictionary.md          # Detailed business logic for each metric
│   └── __init__.py
├── sim/                          # Task 4: Simulation Engine & UI
│   ├── app.py                     # Simulator interactive dashboard (Streamlit)
│   ├── ux_mock.mp4                # UX demonstration video
│   ├── what_if.py                 # Core "What-if" analysis logic
│   ├── experiments/                        # Model training & EDA notebooks
│   │   ├── EDA_and_training_with_resampled_data.ipynb
│   │   │                                     # Test: train models with resampled data
│   │   ├── model_training_with_multiple_models.ipynb
│   │   │                                     # Test: train multiple machine learning models
│   │   └── model_training_with_resampled_data.ipynb
│   │                                         # Pre-train lgbm models for simulator
│   ├── models/                    # Trained LightGBM models (P10, P50, P90)
│   │   ├── lgbm_progress_delta_p10_model.pkl       
│   │   ├── lgbm_progress_delta_p50_model.pkl      
│   │   └── lgbm_progress_delta_p90_model.pkl        
│   └── prepared_data/             # Final feature sets for the simulator
│       └── df_10min_features.csv                    # Resampled data for simulator
├── app.py                        # Main entry point for both task 1&4
├── app_kpis.py                   # KPI dashboard for task 1
├── requirements.txt              # Python dependencies
└── README.md                     # This file - START HERE
```

---

## 🧠 Core Features & Highlights

### 1. KPI Engine (Task 1)

The project implements a **standardized KPI framework** for construction project monitoring.
All KPI definitions, assumptions, and formulas are explicitly documented in:

* `kpis/kpi_dictionary.md`

This ensures:

* Transparency of business logic
* Reproducibility of metric calculations
* Clear separation between data engineering and analytics

---

### 2. Probabilistic Predictive Modeling (LightGBM)

We apply **LightGBM Quantile Regression** to predict short-term project progress changes (`progress_delta`) under uncertainty.

**Key characteristics:**

* Multiple quantile models trained independently:

  * **P10** – optimistic scenario
  * **P50** – median / most likely outcome
  * **P90** – conservative, risk-aware estimate
* Models are pre-trained and loaded at runtime to ensure:

  * ⚡ Fast inference
  * 📉 Stable latency under interactive use

This design supports **uncertainty-aware decision making**, rather than single-point predictions.

---

### 3. Real-Time “What-if” Simulator (Task 4)

The simulation engine allows users to interactively modify project conditions (e.g., workforce levels, utilization assumptions) and immediately observe predicted outcomes.

**Design highlights:**

* Decoupled architecture:

  * `what_if.py`: scenario logic & model inference
  * `app.py`: UI and interaction layer
* Optimized for **sub-300 ms response time** per scenario
* Supports side-by-side comparison of optimistic, median, and risk scenarios

#### 🚀 Demo

To understand how the simulator works and how users can interact with the "What-if" analysis, please refer to the video demonstration:

[https://github.com/hwy225/logpilot-project/blob/task1_weiyun/sim/ux_mock.mp4](https://github.com/hwy225/logpilot-project/blob/task1_weiyun/sim/ux_mock.mp4)

> ⚠️ **Note**
> If the video does not load properly in the README preview, please navigate directly to
> `sim/ux_mock.mp4` in the repository to watch the demo.

---

## 🛠️ Installation & Usage

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the dashboard

```bash
streamlit run app.py
```

### 3. Explore modeling experiments

Refer to:

* `sim/experiments/model_training_with_resampled_data.ipynb`

for details on data resampling strategies, feature engineering, and model training.

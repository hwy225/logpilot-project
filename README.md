# Construction Project Performance & Simulation Platform

This project is a comprehensive data science and machine learning pipeline designed for the construction industry. It covers everything from raw data processing and KPI calculation to predictive modeling and "What-if" scenario simulation.

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
│   ├── experiments/               # Model training & EDA notebooks
│   │   ├──   EDA_and_training_with_resampled_data.ipynb
│   │   ├──   model_training_with_multiple_models.ipynb
│   │   └──   model_training_with_resampled_data.ipynb
│   ├── models/                    # Trained LightGBM models (P10, P50, P90)
│   │   ├── lgbm_progress_delta_p10_model.pkl        # Optimistic prediction (10th percentile)
│   │   ├── lgbm_progress_delta_p50_model.pkl        # Median prediction
│   │   └── lgbm_progress_delta_p90_model.pkl        # Risk-adjusted prediction (90th percentile)
│   └── prepared_data/             # Final feature sets for the simulator
│       └── df_10min_features.csv                    # Feature-engineered data for simulation
├── app.py                        # Main entry point for both task 1&4
├── app_kpis.py                   # KPI dashboard for task 1
├── requirements.txt              # Python dependencies
└── README.md                     # This file - START HERE

```


## 🧠 Core Features

### 1. KPI Engine

The project implements a standardized KPI framework for construction monitoring. Detailed calculation logic for metrics like schedule variance and cost performance can be found in `kpis/kpi_dictionary.md`.

### 2. Predictive Modeling (LightGBM)

We use **Quantile Regression** (LightGBM) to provide probabilistic forecasts for project delays (`progress_delta`):

* **P10 Model**: Optimistic scenario (10th percentile).
* **P50 Model**: Most likely scenario (Median).
* **P90 Model**: Conservative/Risk scenario (90th percentile).

### 3. "What-if" Simulator

The simulator (`sim/app.py`) allows project managers to adjust variables (e.g., resource allocation, site conditions) and see the predicted impact on project completion in real-time.

#### 🚀 Demo

To understand how the simulator works and how users can interact with the "What-if" analysis, please refer to the video demonstration:

<video src="sim/ux_mock.mp4" controls width="800">
Your browser does not support the video tag.
</video>

## 🛠️ Installation & Usage

1. **Install dependencies:**
```bash
pip install -r requirements.txt

```


2. **Run the Dashboard:**
```bash
streamlit run app.py

```


3. **Explore Experiments:**
Check `sim/experiments/model_training_with_resampled_data.ipynb` for details on resampled data and model training.
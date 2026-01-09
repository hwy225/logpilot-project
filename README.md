# Logpilot Build — Construction Analytics Platform

This repository contains a course project for **Logpilot Build**, focusing on transforming raw construction telemetry into **actionable insights, predictive signals, and interactive decision-support tools**.

The project is organized around multiple analytical modules (KPIs, risk prediction, simulation, safety, and reporting).  
Each module is implemented and developed **independently on separate branches**, while this `main` branch provides a **high-level overview** of the project scope and objectives.

---

## 📊 Data Source

The project is based on the **Construction Project Performance Dataset** from Kaggle:

🔗 https://www.kaggle.com/datasets/ziya07/construction-project-performance-dataset

The dataset includes time-series records related to:
- Project progress and task completion
- Cost and schedule deviations
- Resource utilization and operational signals

All raw data files are stored in:

```text
main/data/
````

---

## 🎯 Project Goals

The overall objective is to build a **data-to-insight pipeline** for construction project monitoring, enabling:

- Reliable **project-level KPIs** with data quality guarantees
- **Predictive and probabilistic models** for risk and progress
- A **low-latency “What-if” simulation tool** for operational decision-making
- Clear, interpretable outputs suitable for project managers

---

## 🧩 Implemented Modules (by Task)

The project covers the following tasks defined in the assignment:

1. **Project KPI Roll-ups & Data Health**  
   - KPI aggregation (daily / weekly) and data quality validation  
   - KPI definitions documented in a formal dictionary

2. **Overrun Watch (Early-Warning Signals)**  
   - Classification models to predict short-term cost or schedule overruns

3. **Utilization & Progress Drift Detection**  
   - Anomaly detection for operational inefficiencies and drift patterns

4. **“What-If” Micro-Simulation (Core Focus)**  
   - Interactive scenario analysis for crew and utilization changes  
   - Surrogate models (LightGBM) with uncertainty estimates  
   - Designed for **scenario response time < 300 ms**

5. **Safety Signal Board**  
   - Leading indicators for safety risks using environmental and operational data

6. **Project Scorecard**  
   - Composite performance score aggregating multiple project dimensions

7. **Ops Notes (Data → Insight → Narrative)**  
   - Automated weekly summaries for project managers (LLM-assisted)

---

## 📦 Deliverables Overview

Across all tasks, the project delivers:

- Modular Python pipelines for KPI computation, modeling, and simulation
- Streamlit dashboards for interactive exploration
- Screen-recorded UX demos (videos / GIFs)
- Clear documentation of assumptions, metrics, and limitations

> 🔎 **Note**  
> All detailed implementations, experiments, and dashboards are available in the corresponding **task-specific branches**.  
> Please switch branches to explore individual contributions.

---

## 🧭 How to Navigate This Repository

- `main` branch  
  → Project overview and integration reference  
- Task-specific branches  
  → Full implementations, notebooks, models, and UIs for each task

---

## 🧭 Repository Structure (Main Branch)

```text
main/
├── data/        # Raw dataset from Kaggle
└── README.md    # Project overview (this file)
```

> 🔎 **Note**
> To explore implementations, experiments, models, and dashboards,
> please switch to the relevant **task-specific branches**.

---

## 🧑‍🏫 Intended Audience

This project is designed for:
- Course evaluation and academic review
- Demonstration of applied data science & ML skills
- Exploration of decision-support tooling in construction analytics


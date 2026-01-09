# Task 5: Safety Signal Board - Leading Indicators

**Separate workspace from Task 2 (Overrun Prediction)**

---

## Quick Start

1. **Open the notebook:**
   ```bash
   cd safety/
   jupyter notebook safety_leading_indicators.ipynb
   ```

2. **Run all cells** in sequence (or use "Run All")

3. **Expected outputs:**
   - Trained safety incident prediction model
   - 5 visualization plots in `saved_safety_models/`
   - Model artifacts (`.pkl` files)

---

## What This Does

Predicts **next-day safety risk** using leading indicators:
- 🌡️ **Environmental stress**: Heat index (temp + humidity)
- ⚙️ **Equipment stress**: Vibration patterns and spikes
- 👷 **Human factors**: Night shifts, worker density
- 📊 **Historical patterns**: LAG features (previous 7 days)

**Goal:** Alert HSE teams 24 hours in advance with **high recall** (don't miss high-risk days!)

---

## Folder Structure

```
safety/
├── README.md                           ← You are here
├── safety_leading_indicators.ipynb     ← Main notebook (12 sections, fully coded)
└── saved_safety_models/                ← Model outputs (created after running)
    ├── [model_name]_safety_model.pkl   ← Trained model
    ├── safety_scaler.pkl               ← Feature scaler
    ├── model_metadata.pkl              ← Feature names, metrics
    ├── roc_curve.png                   ← Model performance
    ├── shap_summary.png                ← Feature importance
    ├── shap_importance.png             ← Mean SHAP values
    ├── partial_dependence.png          ← Leading indicator effects
    └── recall_at_k.png                 ← HSE efficiency curve
```

---

## What's Different from Task 2?

| Aspect | Task 2 (Overrun) | Task 5 (Safety) |
|--------|------------------|-----------------|
| **Target** | TIME/COST overrun (7% threshold) | Safety incidents (median threshold) |
| **Optimization** | Accuracy, Precision@k | **Recall** (don't miss high-risk days!) |
| **Features** | Efficiency KPIs, LAG | Leading indicators, LAG |
| **Evaluation** | Precision@k (top-k projects) | **Recall@k** (catch % of incidents) |
| **Stakeholder** | Project Managers | HSE Teams |
| **Folder** | `models/` | `safety/` (separate!) |

---

## Learnings from Task 2 Applied Here

✅ **Daily Aggregation:** Reduces noise, aligns with management  
✅ **LAG Features:** Most powerful (1, 2, 3, 5, 7 days)  
✅ **Chronological Split:** 68%/15%/17% prevents leakage  
✅ **class_weight='balanced':** Handles imbalanced classes  
✅ **SHAP Interpretability:** Builds stakeholder trust  
✅ **Start Simple:** LR baseline → XGBoost if needed  

---

## Notebook Sections (12 Total)

1. **Setup & Data Loading** - Import libraries, load data
2. **Daily Aggregation** - Hourly → daily (like Task 2)
3. **Feature Engineering** - Heat index, vibration, night shifts, LAG
4. **Target Definition** - High-risk day = incidents > median
5. **Train/Val/Test Split** - Chronological (68%/15%/17%)
6. **Feature Selection** - Top 15 by correlation
7. **Model Training** - LR + XGBoost with recall focus
8. **SHAP Interpretability** - Explain predictions
9. **Partial Dependence** - Leading indicator effects
10. **Recall@k Analysis** - HSE efficiency metrics
11. **Save Models** - Pickle all artifacts
12. **Summary** - Results and next steps

**Each section has:**
- Markdown explanations
- Complete working code
- Visualizations
- Interpretations

---

## Questions to Ask After Running

The notebook ends with **10 questions** you can ask me about:
- Why median threshold?
- Why recall > precision for safety?
- How LAG features work
- What is heat index?
- How to interpret SHAP plots
- Why standardize features?
- What is class_weight='balanced'?
- Could we ensemble models?
- How to deploy for real-time alerts?
- Can we add more features?

---

## Expected Results

**Model Performance:**
- AUC: ~0.65-0.80 (exact value after running)
- Recall: **Prioritized** (minimize false negatives)
- Precision: Secondary (false positives = extra checks, acceptable)

**Top Features:**
- `safety_incidents_lag1` (yesterday's incidents)
- `vibration_level_lag1/2` (equipment stress)
- `heat_index` (environmental stress)
- `night_shift_pct` (human factors)
- `worker_density` (crowding risk)

**Visualizations:**
- ROC curve showing model performance
- SHAP plots showing feature importance and directionality
- Partial Dependence showing actionable thresholds
- Recall@k showing HSE team efficiency

---

## Time Estimate

- **First run:** 15-20 minutes (includes reading explanations)
- **Execution only:** 3-5 minutes (all cells)
- **Review + questions:** 30-60 minutes

**Total for Task 5:** 3-4 hours (including feature engineering, model training, interpretation, documentation)

---

## Documentation

- **Deliverable:** `docs/deliverables/TASK5_SAFETY_DELIVERABLE.md`
- **This README:** Quick reference
- **Notebook markdown:** Detailed explanations in each section

---

## Next Steps (Optional)

1. **Run the notebook** - Execute all cells, review results
2. **Ask questions** - About any section you want to understand better
3. **Experiment** - Try different thresholds, features, models
4. **Deploy** - Build API for daily alerts (like Task 2's `overrun_api.py`)
5. **Extend** - Add more features, multi-project data, hourly predictions

---

**Ready to run? Open `safety_leading_indicators.ipynb` and start from Section 1!**

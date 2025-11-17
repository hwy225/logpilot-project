# 🎯 Threshold Change: 0% → 15% for Significant Overruns

## Date: November 12, 2025

## Reason for Change

### Previous Results (0% Threshold):
- **Target Flip Rate**: ~50% (time), ~44% (cost)
- **Test Performance**: 
  - Logistic Regression: 66.7% accuracy, 0.5 AUC (TIME)
  - Severe overfitting across all models (95-100% train → 33-67% test)
- **Problem**: Any deviation >0% was flagged as overrun, creating noisy targets

### Decision:
Change to **15% deviation threshold** to:
1. Capture only **significant/meaningful overruns** (business-relevant)
2. Reduce **target noise** and improve stability
3. Create **clearer class separation** between normal and problematic days
4. Improve **model learning** and generalization

---

## Changes Made

### File: `models/EDA_corr.ipynb`

#### 1. Target Generation Cell (Cell 23)
**Before:**
```python
time_threshold = 0
cost_threshold = 0
```

**After:**
```python
time_threshold = 0.15  # 15% deviation threshold for time
cost_threshold = 0.15  # 15% deviation threshold for cost
```

**What This Means:**
- **Time overrun**: Only flagged if next day's time_deviation > 15%
- **Cost overrun**: Only flagged if next day's cost_deviation > 15%
- **Example**: 
  - Project planned for 10 days, actual is 11.5 days → 15% time overrun ✅ flagged
  - Project planned for 10 days, actual is 10.5 days → 5% time overrun ❌ not flagged

#### 2. Added Target Distribution Preview
New code displays:
- How many cases exceed 15% threshold
- Class balance with new threshold
- Helps validate threshold is not too strict or too loose

#### 3. Updated Diagnostic Section Headers
- Changed to "15% Threshold" to clarify context
- Updated interpretation notes to mention expected improvements

---

## Expected Improvements

### 1. **Target Stability (Most Important)**
- **Before**: 50% flip rate (targets change every ~2 days)
- **Expected**: <30% flip rate (more consecutive days with same status)
- **Why**: 15% is a larger threshold, so status changes less frequently

### 2. **Class Balance**
- **Before**: ~65% positive (overrun), ~35% negative
- **Expected**: ~30-40% positive (significant overruns are rarer)
- **Why**: Fewer days exceed 15% threshold than 0% threshold

### 3. **Model Performance**
- **Before**: Severe overfitting (train 95% → test 50%)
- **Expected**: 
  - Less overfitting (clearer signal to learn)
  - Better test generalization
  - More stable predictions across models
  - Ensemble methods may actually help now

### 4. **Feature Correlations**
- **Before**: Max correlation ~0.35 (moderate)
- **Expected**: Similar or better (15% events may have stronger feature signals)

### 5. **Business Value**
- **Before**: Predicting any deviation (including trivial ones)
- **After**: Predicting **significant overruns** that need intervention
- **Practical**: 15% overrun is meaningful to project managers

---

## How to Run the Updated Pipeline

### Step 1: Re-run EDA_corr.ipynb
```bash
# Open EDA_corr.ipynb
# Run all cells from top to bottom
# Expected output:
#   - Target generation will show new distribution
#   - Diagnostics will show improved flip rate
#   - Feature selection may change slightly
```

**Key Cells to Watch:**
- **Cell 23**: Check target counts (should see fewer positive cases)
- **Cell 26** (Diagnostic 1): Check flip rate (should be <40%)
- **Cell 27** (Diagnostic 2): Check correlations (may improve)
- **Cell 28** (Diagnostic 3): Check class balance (will be more imbalanced)

### Step 2: Re-run model_training.ipynb
```bash
# Open model_training.ipynb
# Run all cells from top to bottom
# Expected improvements:
#   - Reduced train-test gap (less overfitting)
#   - Better test AUC scores (>0.5 hopefully)
#   - Ensemble methods may show value
```

**Key Sections to Compare:**
- **Section 6.1**: TIME model metrics (compare to previous run)
- **Section 6.2**: COST model metrics (compare to previous run)
- **Section 11**: Final summary (see if ensembles outperform baseline)

---

## Validation Checklist

After re-running, verify:

### ✅ Data Quality (EDA_corr.ipynb)
- [ ] Target flip rate < 40% (preferably <30%)
- [ ] Class balance ratio between 0.3-3.0
- [ ] At least 10+ positive cases for each target (not too rare)
- [ ] Feature correlations still meaningful (>0.15)

### ✅ Model Performance (model_training.ipynb)
- [ ] Test AUC > 0.5 for at least one model
- [ ] Train-test gap < 30% (e.g., train 85% → test 60%)
- [ ] Ensemble shows improvement over baseline
- [ ] Confusion matrices show balanced predictions

### ⚠️ Potential Issues
- **Too few positives**: If <10 positive cases, threshold is too strict
  - Solution: Try 10% threshold instead
- **Still high flip rate**: If >40%, data is inherently volatile
  - Solution: Accept limitations or try different features
- **Class imbalance**: If <20% positive, need stronger class weights
  - Solution: Already handled with `class_weight='balanced'`

---

## Comparison: 0% vs 15% Threshold

| Metric | 0% Threshold | 15% Threshold (Expected) |
|--------|--------------|--------------------------|
| **Target Stability** | 50% flip rate | <30% flip rate |
| **Positive Cases** | ~65% | ~30-40% |
| **Business Meaning** | Any deviation | Significant overruns |
| **Model Learning** | Noisy signal | Clearer signal |
| **Test AUC (TIME)** | 0.5 (LR) | >0.6 (hopefully) |
| **Overfitting** | Severe (train 95%→test 50%) | Reduced (train 75%→test 60%) |
| **Ensemble Value** | No improvement | May show benefit |

---

## Next Steps After Validation

### If Results Improve (Expected):
1. ✅ Document final model performance
2. ✅ Extract SHAP explanations for best model
3. ✅ Create business-ready predictions
4. ✅ Write up findings and limitations

### If Results Still Poor:
1. Try **10% threshold** (middle ground)
2. Try **different target**: Predict acceleration/deceleration rather than absolute overrun
3. Consider **external data**: Weather, holidays, material prices
4. Accept **data limitations**: 34 samples is genuinely small

---

## Technical Notes

### Why 15%?
- **Industry standard**: 10-20% variance is common threshold in construction
- **Statistical**: Large enough to be meaningful, small enough to have cases
- **Balance**: Not too strict (enough positive cases), not too loose (clear signal)

### Alternative Thresholds to Consider:
- **10%**: More lenient, more positive cases, may still be noisy
- **20%**: Stricter, fewer positive cases, may be too rare
- **Adaptive**: Use percentile-based threshold (e.g., top 30% of deviations)

### Code Impact:
- **Single line change**: Just the threshold values
- **No architecture changes**: All models and pipelines unchanged
- **Fast iteration**: Can try different thresholds easily

---

## Questions to Answer After Re-running:

1. What is the new target flip rate? (Diagnostic 1)
2. How many positive cases do we have? (Target generation output)
3. What is the new class balance ratio? (Diagnostic 3)
4. Did test AUC improve? (Model evaluation)
5. Do ensembles show benefit now? (Final comparison)
6. Are predictions more stable? (Compare across runs)

---

## Conclusion

The 15% threshold change is a **data quality improvement** that should:
- ✅ Reduce noise in targets
- ✅ Improve model learning
- ✅ Make predictions more meaningful
- ✅ Better align with business needs

**Expected outcome**: More robust models that predict **significant overruns** rather than trivial fluctuations.

**Remember**: This is still a small dataset (34 samples), so perfect performance is unrealistic. The goal is **meaningful improvement** and **business-relevant predictions**.

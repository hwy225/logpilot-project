# Future: Synthetic Data Generation for Construction Projects

## Problem Statement

Current dataset has only **34 daily samples** (23 training), which limits model performance:
- Overfitting risk with complex models
- Limited ability to learn patterns
- Difficult to validate robustness
- Can't explore hyperparameter tuning fully

## Synthetic Data Generation Approaches

### 🎯 Option 1: Time Series Augmentation (SAFEST)

**Method**: Create variations of existing daily sequences
```python
# Techniques:
- Jittering: Add small random noise to features (~5% std)
- Time warping: Stretch/compress time sequences slightly
- Window slicing: Create overlapping subsequences
- Interpolation: Generate intermediate points between days
```

**Pros:**
- Preserves domain constraints
- Low risk of unrealistic data
- Easy to implement

**Cons:**
- Limited diversity
- May not explore new patterns
- Still constrained by original 35 days

**Best for:** 
- Immediate need (quick 2-3x data increase)
- Conservative approach

---

### 🎯 Option 2: SMOTE-like for Time Series (MODERATE)

**Method**: Synthetic Minority Over-sampling adapted for temporal data
```python
from imblearn.over_sampling import SMOTE
from tsaug import TimeWarp, Crop

# Apply SMOTE on lag features
# Preserve temporal ordering
# Generate new sequences between similar days
```

**Pros:**
- Balanced classes automatically
- Proven technique
- Can generate diverse samples

**Cons:**
- May create unrealistic combinations
- Needs careful validation
- Temporal dependencies may break

**Best for:**
- Class imbalance problems
- Need 5-10x more data
- When willing to validate synthetic samples

---

### 🎯 Option 3: GAN/VAE for Construction Data (ADVANCED)

**Method**: Train generative model on existing data
```python
# TimeGAN or similar
- Learn distribution of construction project patterns
- Generate entirely new project sequences
- Condition on project characteristics
```

**Pros:**
- Can create realistic novel scenarios
- Large data generation possible
- Learns complex patterns

**Cons:**
- Needs more data to train well (catch-22)
- Risk of mode collapse
- Difficult to validate quality
- Requires significant effort

**Best for:**
- Long-term solution
- Research project
- When you can collect ~100+ real samples first

---

### 🎯 Option 4: Physics/Rule-Based Simulation (DOMAIN-DRIVEN)

**Method**: Create synthetic data using construction domain knowledge
```python
# Example rules:
- If worker_count increases → energy_consumption increases (correlation)
- If material_shortage → task_progress slows → time_deviation increases
- Weather effects: temperature/humidity impact progress
- Weekly patterns: 5-day work week, weekend effects
```

**Pros:**
- Physically realistic
- Can encode domain expertise
- Explainable generation process
- No training needed

**Cons:**
- Requires domain expert input
- May miss unexpected patterns
- Time-consuming to build

**Best for:**
- When domain experts available
- Need explainable synthetic data
- Creating training scenarios

---

## Recommended Approach (Staged)

### 🏗️ Phase 1: Quick Win (Now → 1 week)
**Jittering + Time Warping**
```python
# Implementation:
import numpy as np
from tsaug import AddNoise, TimeWarp

# For each original sequence:
# 1. Add Gaussian noise (σ = 0.05 * feature_std)
# 2. Time warp (stretch/compress by ±10%)
# 3. Generate 2-3 variants per original

# Result: 34 → ~100 samples
```

**Validation:**
- Compare feature distributions (original vs synthetic)
- Check correlation matrices match
- Ensure no unrealistic values
- Visual inspection of time series

---

### 🏗️ Phase 2: Balanced Data (1-2 weeks)
**SMOTE + Domain Rules**
```python
# Implementation:
1. Apply SMOTE on lag features for minority class
2. Apply domain constraints:
   - energy_per_worker ratios stay realistic
   - material_usage can't be negative
   - task_progress is monotonic increasing
3. Generate balanced dataset

# Result: ~200-300 samples with balanced classes
```

**Validation:**
- Train model on synthetic only → test on real holdout
- Measure distribution shift (KL divergence)
- Expert review of edge cases

---

### 🏗️ Phase 3: Long-term Solution (2-3 months)
**Physics-Based Simulator**
```python
# Implementation:
1. Interview domain experts
2. Build rule-based simulator:
   - Project initialization (size, budget, timeline)
   - Daily update rules (resource allocation, progress)
   - Risk events (weather, delays, shortages)
   - Cost/time accumulation logic
3. Generate diverse project scenarios

# Result: Unlimited realistic data
```

**Validation:**
- Compare with real project data
- Domain expert validation
- Statistical tests (distribution matching)

---

## Critical Considerations

### ⚠️ Validation is KEY
- **Never mix synthetic with test set**
- Train on synthetic → validate on real
- Compare performance: (real → real) vs (synthetic → real)
- If synthetic hurts performance, discard

### ⚠️ Domain Constraints
Must preserve:
- `task_progress` is monotonic (0 → 100%)
- `worker_count` is integer ≥ 0
- `temperature`, `humidity` in realistic ranges
- Correlations: energy ∝ workers, material ∝ progress

### ⚠️ Temporal Dependencies
Must maintain:
- Lag relationships (today depends on yesterday)
- Weekly patterns (5-day work weeks)
- Cumulative effects (costs/time accumulate)

### ⚠️ Class Balance
Synthetic data should:
- Not artificially inflate accuracy
- Preserve natural overrun rates (~40-60% at 7% threshold)
- Create diverse failure scenarios

---

## Metrics to Track

Before/after synthetic data generation:

| Metric | Before (Real Only) | After (+ Synthetic) | Goal |
|--------|-------------------|---------------------|------|
| Training samples | 23 | 100-200 | 5-10x increase |
| Test accuracy (real) | 50% | ??? | Maintain or improve |
| Test AUC (real) | 0.75 | ??? | ≥ 0.75 |
| Overfitting gap | High | ??? | Reduce |
| Feature importance | ??? | ??? | Stay stable |

---

## Quick Start Code Template

```python
# Option 1: Simple Jittering (Try this first!)

import numpy as np
import pandas as pd

def jitter_data(df, noise_level=0.05, n_augmented=2):
    """
    Create augmented versions of time series data with noise.
    
    Args:
        df: Original dataframe (34 samples)
        noise_level: Std of Gaussian noise (relative to feature std)
        n_augmented: Number of synthetic samples per original
    
    Returns:
        Augmented dataframe
    """
    synthetic_data = []
    
    for i in range(len(df)):
        # Keep original
        synthetic_data.append(df.iloc[i].copy())
        
        # Generate variants
        for j in range(n_augmented):
            sample = df.iloc[i].copy()
            
            # Add noise to numeric features only
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if col not in ['time_overrun_next', 'cost_overrun_next']:
                    noise = np.random.normal(0, noise_level * df[col].std())
                    sample[col] = sample[col] + noise
            
            # Keep targets unchanged
            synthetic_data.append(sample)
    
    return pd.DataFrame(synthetic_data)

# Usage:
df_augmented = jitter_data(df_model, noise_level=0.05, n_augmented=2)
print(f"Original: {len(df_model)} samples")
print(f"Augmented: {len(df_augmented)} samples")

# CRITICAL: Split BEFORE augmentation
# Train: augment → 23 → ~70 samples
# Val/Test: NO augmentation (real data only)
```

---

## Decision Framework

**Use synthetic data if:**
- ✅ Real data collection is slow/expensive
- ✅ You have domain expertise to validate
- ✅ Current model shows high variance (overfitting)
- ✅ You can hold out real test set

**Don't use synthetic data if:**
- ❌ Can collect more real data easily
- ❌ Can't validate synthetic samples
- ❌ Current model already works well
- ❌ Domain is too complex to simulate

---

## Next Steps

1. **First**: Stabilize current model with derived KPIs + lags
2. **Then**: Try simple jittering (Phase 1)
3. **Validate**: Compare (real→real) vs (synthetic+real→real)
4. **If successful**: Move to Phase 2
5. **Long-term**: Build domain simulator (Phase 3)

---

**Note**: This is a future exploration topic. Current focus is on stabilizing the model with:
- ✅ 7% threshold
- ✅ Top 10 features
- ✅ Derived KPIs + Lag features (NO rolling windows)

---

**Date**: November 12, 2025  
**Status**: Ideas for future work  
**Priority**: Medium (after current model is stable)

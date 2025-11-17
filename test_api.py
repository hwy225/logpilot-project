"""
Test Script for Overrun Watch API
==================================
Quick validation that the API loads and works correctly.
"""

import sys
sys.path.append('models')

from models.overrun_api import OverrunPredictor
import pickle
import pandas as pd

def test_api():
    """Run comprehensive API tests."""
    
    print("=" * 80)
    print("TESTING OVERRUN WATCH API")
    print("=" * 80)
    
    # Test 1: Initialize predictor
    print("\n[TEST 1] Initializing predictor...")
    try:
        predictor = OverrunPredictor(model_dir='models/saved_models')
        print("✅ Predictor initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize predictor: {e}")
        return False
    
    # Test 2: Load test data
    print("\n[TEST 2] Loading test data...")
    try:
        with open('models/prepared_data/modeling_datasets.pkl', 'rb') as f:
            datasets = pickle.load(f)
        
        X_test_time = datasets['X_test_time']
        X_test_cost = datasets['X_test_cost']
        y_test_time = datasets['y_test_time']
        y_test_cost = datasets['y_test_cost']
        
        print(f"✅ Test data loaded: {len(X_test_time)} samples")
        print(f"   TIME features: {X_test_time.shape[1]}")
        print(f"   COST features: {X_test_cost.shape[1]}")
    except Exception as e:
        print(f"❌ Failed to load test data: {e}")
        return False
    
    # Test 3: Single TIME prediction
    print("\n[TEST 3] Testing TIME overrun prediction...")
    try:
        sample = X_test_time.iloc[0:1]
        result = predictor.predict_time_overrun(sample, project_id="TEST_001")
        
        print("✅ TIME prediction successful")
        print(f"   Project: {result['project_id']}")
        print(f"   Prediction: {result['prediction_label']}")
        print(f"   Confidence: {result['confidence_pct']}")
        print(f"   Status: {result['model_status']}")
    except Exception as e:
        print(f"❌ TIME prediction failed: {e}")
        return False
    
    # Test 4: Single COST prediction
    print("\n[TEST 4] Testing COST overrun prediction...")
    try:
        sample = X_test_cost.iloc[0:1]
        result = predictor.predict_cost_overrun(sample, project_id="TEST_001")
        
        print("✅ COST prediction successful")
        print(f"   Project: {result['project_id']}")
        print(f"   Prediction: {result['prediction_label']}")
        print(f"   Confidence: {result['confidence_pct']}")
        print(f"   Status: {result['model_status']}")
    except Exception as e:
        print(f"❌ COST prediction failed: {e}")
        return False
    
    # Test 5: Batch ranking
    print("\n[TEST 5] Testing project ranking...")
    try:
        # Create list of projects
        projects = []
        for i in range(min(6, len(X_test_time))):
            projects.append({
                'project_id': f'Project_{i+1}',
                'features': X_test_time.iloc[i:i+1]
            })
        
        ranked = predictor.rank_projects(projects, target='time', top_k=3)
        
        print("✅ Project ranking successful")
        print(f"   Ranked {len(projects)} projects, showing top 3:")
        print(ranked.to_string(index=False))
    except Exception as e:
        print(f"❌ Project ranking failed: {e}")
        return False
    
    # Test 6: Feature importance
    print("\n[TEST 6] Testing feature importance...")
    try:
        importance_time = predictor.get_feature_importance('time', top_n=5)
        importance_cost = predictor.get_feature_importance('cost', top_n=5)
        
        print("✅ Feature importance successful")
        print(f"\n   Top 5 TIME features:")
        for idx, row in importance_time.iterrows():
            print(f"     {idx+1}. {row['feature']}: {row['importance']:.4f}")
        
        print(f"\n   Top 5 COST features:")
        for idx, row in importance_cost.iterrows():
            print(f"     {idx+1}. {row['feature']}: {row['importance']:.4f}")
    except Exception as e:
        print(f"❌ Feature importance failed: {e}")
        return False
    
    # Test 7: Alert generation
    print("\n[TEST 7] Testing alert generation...")
    try:
        sample = X_test_time.iloc[0:1]
        result = predictor.predict_time_overrun(sample, project_id="ALERT_TEST")
        
        # Test different formats
        alert_text = predictor.generate_alert(result, format='text')
        alert_md = predictor.generate_alert(result, format='markdown')
        alert_html = predictor.generate_alert(result, format='html')
        
        print("✅ Alert generation successful")
        print(f"   Text alert: {len(alert_text)} characters")
        print(f"   Markdown alert: {len(alert_md)} characters")
        print(f"   HTML alert: {len(alert_html)} characters")
        
        print("\n   Sample alert (text):")
        print(alert_text)
    except Exception as e:
        print(f"❌ Alert generation failed: {e}")
        return False
    
    # Test 8: Combined prediction
    print("\n[TEST 8] Testing combined TIME + COST prediction...")
    try:
        sample_time = X_test_time.iloc[0:1]
        sample_cost = X_test_cost.iloc[0:1]
        
        result = predictor.predict_both(sample_time, sample_cost, project_id="COMBINED_TEST")
        
        print("✅ Combined prediction successful")
        print(f"   TIME: {result['time_overrun']['prediction_label']} "
              f"({result['time_overrun']['confidence_pct']})")
        print(f"   COST: {result['cost_overrun']['prediction_label']} "
              f"({result['cost_overrun']['confidence_pct']})")
        print(f"   Overall Risk: {result['overall_risk_level']}")
    except Exception as e:
        print(f"❌ Combined prediction failed: {e}")
        return False
    
    # All tests passed
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80)
    print("\nAPI is ready for production use:")
    print("  ✅ Models load correctly")
    print("  ✅ Predictions work for both TIME and COST")
    print("  ✅ Ranking and batch processing functional")
    print("  ✅ Feature importance extraction working")
    print("  ✅ Alert generation in multiple formats")
    print("  ✅ Combined predictions supported")
    print("=" * 80)
    
    return True


if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)

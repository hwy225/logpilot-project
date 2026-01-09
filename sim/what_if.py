import pandas as pd
from pathlib import Path
import joblib

def build_scenario_input(current_state_df: pd.DataFrame, 
                         worker_delta: int = 0, 
                         utilization_multiplier: float = 1.0) -> pd.DataFrame:
    """
    Builds the input DataFrame for the What-If scenario based on the current state and specified changes.
    
    Args:
        current_state_df: DataFrame containing all features at the current time t (single-row DataFrame).
        worker_delta: Change in the number of workers (e.g., +2).
        utilization_multiplier: Change in equipment utilization rate (e.g., 1.10).
        
    Returns:
        pd.DataFrame: Input data for the model prediction at the next time step t+1 (single-row).
    """
    
    # Copy current state as the baseline for the next time step
    X_scenario = current_state_df.copy()

    # ----------------------------------------------------
    # 1. Apply What-If changes (features at time t+1)
    # ----------------------------------------------------
    X_scenario['worker_count'] = current_state_df['worker_count'] + worker_delta
    X_scenario['equipment_utilization_rate'] = current_state_df['equipment_utilization_rate'] * utilization_multiplier

       
    # Ensure column order and names are consistent with model training
    return X_scenario

def predict_scenario(X_scenario: pd.DataFrame, 
                     model_q05, model_q50, model_q95) -> dict:
    """
    Performs quantile predictions for the What-If scenario.
    """
    # Predict three quantiles
    pred_q05 = model_q05.predict(X_scenario)[0]
    pred_q50 = model_q50.predict(X_scenario)[0]
    pred_q95 = model_q95.predict(X_scenario)[0]
    
    return {
        'point_estimate': pred_q50,
        'lower_bound': pred_q05,
        'upper_bound': pred_q95
    }

def what_if_api(current_state_df: pd.DataFrame, 
                worker_change: int, 
                utilization_change: float) -> dict:
    
    # load models
    current_dir = Path(__file__).parent
    model_folder = current_dir / "models"
    progress_models = {
        'q10': joblib.load(model_folder / 'lgbm_progress_delta_p10_model.pkl'),
        'q50': joblib.load(model_folder / 'lgbm_progress_delta_p50_model.pkl'),
        'q90': joblib.load(model_folder / 'lgbm_progress_delta_p90_model.pkl')
    }

    X_scenario = build_scenario_input(
        current_state_df=current_state_df, 
        worker_delta=worker_change, 
        utilization_multiplier=utilization_change
    )
    # predict progress delta
    progress_results = predict_scenario(
        X_scenario, 
        progress_models['q10'], progress_models['q50'], progress_models['q90']
    )
    
    # Progress Shift
    output = {
        "progress_delta_estimate": progress_results['point_estimate'],
        "progress_delta_90_pi": (
            progress_results['lower_bound'],
            progress_results['upper_bound']
        ),
    }
    
    return output


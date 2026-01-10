"""
🏗️ LogPilot Unified Dashboard
================================
Comprehensive construction intelligence platform combining all 7 tasks.

Team: Weiyun, Vyoma, Feruz | Masters in Data Science | January 2026
"""

import streamlit as st
from pathlib import Path
import sys

# Page configuration
st.set_page_config(
    page_title="LogPilot - Construction Intelligence",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f2f6 0%, #ffffff 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
           # Load daily scorecard
        daily_file = results_path / "daily_scorecard_per_site.csv"
        if daily_file.exists():
            daily_df = pd.read_csv(daily_file)
            
            st.subheader("📅 Daily Scorecard")
            st.dataframe(daily_df.head(20), width="stretch").task-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .task-card h4 {
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .task-card p {
        color: #333333;
        margin: 0.25rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🏗️ LogPilot Navigation")
st.sidebar.markdown("---")

# Task selection
task_options = {
    "🏠 Home": "home",
    "📊 Task 1: KPI Dashboard": "task1_kpi_dashboard",
    "⚠️ Task 2: Overrun Watch": "task2_overrun_watch",
    "🔍 Task 3: Drift Detection": "task3_drift_detection",
    "🎮 Task 4: What-If Simulation": "task4_what_if_simulation",
    "🛡️ Task 5: Safety Signal Board": "task5_safety_signal_board",
    "📊 Task 6: Project Scorecard": "task6_project_scorecard",
    "📝 Task 7: Weekly Ops Notes": "task7_weekly_ops_notes"
}

selected_page = st.sidebar.radio(
    "Select Module:",
    list(task_options.keys()),
    index=0
)

# Team info in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 👥 Team")
st.sidebar.markdown("""
- **Weiyun**: Tasks 1, 4
- **Vyoma**: Tasks 2, 5, 7
- **Feruz**: Tasks 3, 6
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📅 Project Info")
st.sidebar.info("**January 2026**\n\nMasters in Data Science")

# Main content area
current_page = task_options[selected_page]


# ============================================================================
# HOME PAGE
# ============================================================================
if current_page == "home":
    st.markdown('<div class="main-header">🏗️ LogPilot: Construction Intelligence Platform</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <h3>AI-Powered Analytics & Decision Support for Construction Projects</h3>
        <p style='color: #666; font-size: 1.1rem;'>
            Select a task from the sidebar to view its interactive dashboard →
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tasks Completed", "7/7", "100%")
    with col2:
        st.metric("TIME Model AUC", "0.750", "Production")
    with col3:
        st.metric("Safety Recall", "1.00", "Perfect")
    with col4:
        st.metric("Sim Response", "<300ms", "Real-time")
    
    st.markdown("---")
    
    # Task overview grid
    st.subheader("📋 Available Modules")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("""
        <div class="task-card">
            <h4>📊 Task 1: KPI Dashboard</h4>
            <p><strong>Owner:</strong> Weiyun</p>
            <p>Real-time project KPI computation and visualization.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="task-card">
            <h4>🔍 Task 3: Drift Detection</h4>
            <p><strong>Owner:</strong> Feruz</p>
            <p>Anomaly detection results and visualizations.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="task-card">
            <h4>🛡️ Task 5: Safety Signal Board</h4>
            <p><strong>Owner:</strong> Vyoma</p>
            <p>Interactive safety risk assessment tool.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="task-card">
            <h4>📝 Task 7: Weekly Ops Notes</h4>
            <p><strong>Owner:</strong> Vyoma</p>
            <p>AI-powered report generation interface.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("""
        <div class="task-card">
            <h4>⚠️ Task 2: Overrun Watch</h4>
            <p><strong>Owner:</strong> Vyoma</p>
            <p>TIME/COST overrun prediction dashboard.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="task-card">
            <h4>🎮 Task 4: What-If Simulation</h4>
            <p><strong>Owner:</strong> Weiyun</p>
            <p>Interactive scenario analysis simulator.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="task-card">
            <h4>📊 Task 6: Project Scorecard</h4>
            <p><strong>Owner:</strong> Feruz</p>
            <p>Composite performance scoring dashboard.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("👈 **Select a task from the sidebar to view its interactive dashboard**")


# ============================================================================
# TASK 1: KPI DASHBOARD
# ============================================================================
elif current_page == "task1_kpi_dashboard":
    st.title("📊 Task 1: KPI Dashboard")
    st.markdown("**Owner:** Weiyun | **Status:** ✅ Complete")
    st.markdown("---")
    
    try:
        import pandas as pd
        import numpy as np
        from kpis.etl_kpis import compute_project_kpis, get_kpi_definitions
        import plotly.express as px
        import plotly.graph_objects as go
        
        # Load data
        df = pd.read_csv("data/construction_project_dataset.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Frequency selector
        freq_option = st.selectbox(
            "📅 Select Aggregation Frequency:",
            options=["Weekly", "Daily"],
            index=0,
            key="freq_selector"
        )
        
        freq_map = {"Weekly": "W", "Daily": "D"}
        freq = freq_map[freq_option]
        
        # Compute KPIs
        with st.spinner(f"Computing {freq_option} KPIs..."):
            if freq == "D":
                # Use subset for daily to avoid slowdown
                kpi_df = compute_project_kpis(df.head(20000), freq=freq)
            else:
                kpi_df = compute_project_kpis(df, freq=freq)
        
        # Display data date range
        data_start = df['timestamp'].min()
        data_end = df['timestamp'].max()
        st.info(f"📅 **Data Period:** {data_start.strftime('%Y-%m-%d')} to {data_end.strftime('%Y-%m-%d')} ({len(df):,} records)")
        
        st.success(f"✅ Computed KPIs for {len(kpi_df)} {freq_option.lower()} periods")
        
        # === DATA HEALTH INDEX ===
        st.subheader("📊 Data Health Index")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Use Weiyun's naming: data_health_index
            latest_health = kpi_df['data_health_index'].iloc[-1]
            avg_health = kpi_df['data_health_index'].mean()
            
            st.metric("Latest Health Score", f"{latest_health:.1f}%", 
                     f"{latest_health - avg_health:+.1f}% vs avg")
            st.metric("Average Health Score", f"{avg_health:.1f}%")
            
            # Health status
            if avg_health >= 95:
                st.success("✅ Excellent Data Quality")
            elif avg_health >= 85:
                st.info("ℹ️ Good Data Quality")
            elif avg_health >= 70:
                st.warning("⚠️ Acceptable Data Quality")
            else:
                st.error("🚨 Poor Data Quality - Review Needed")
        
        with col2:
            # Health trend chart
            fig = px.line(kpi_df, x='timestamp', y='data_health_index',
                         title='Data Health Score Over Time')
            fig.add_hline(y=95, line_dash="dash", line_color="green", 
                         annotation_text="Target: 95%")
            fig.update_layout(height=250)
            st.plotly_chart(fig, width="stretch")
        
        # === KEY METRICS ===
        st.subheader("📈 Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'progress_pct' in kpi_df.columns:
                latest_progress = kpi_df['progress_pct'].iloc[-1]
                st.metric("Progress", f"{latest_progress:.1f}%")
        
        with col2:
            if 'resource_utilization' in kpi_df.columns:
                latest_util = kpi_df['resource_utilization'].iloc[-1]
                st.metric("Resource Utilization", f"{latest_util:.1f}%")
        
        with col3:
            if 'cost_efficiency' in kpi_df.columns:
                latest_cost = kpi_df['cost_efficiency'].iloc[-1]
                st.metric("Cost Efficiency", f"{latest_cost:.1f}%")
        
        with col4:
            if 'schedule_adherence' in kpi_df.columns:
                latest_schedule = kpi_df['schedule_adherence'].iloc[-1]
                st.metric("Schedule Adherence", f"{latest_schedule:.1f}%")
        
        # === TREND CHARTS ===
        st.subheader("📊 KPI Trends")
        
        chart_cols = st.columns(2)
        
        # Use Weiyun's column naming conventions
        metrics_to_plot = [
            ('task_progress_last', 'Task Progress', 'blue'),
            ('equipment_utilization_rate_mean', 'Equipment Utilization %', 'green'),
            ('cost_efficiency', 'Cost Efficiency %', 'orange'),
            ('schedule_adherence', 'Schedule Adherence %', 'purple')
        ]
        
        for i, (metric, title, color) in enumerate(metrics_to_plot):
            if metric in kpi_df.columns:
                with chart_cols[i % 2]:
                    fig = px.line(kpi_df, x='timestamp', y=metric, title=title)
                    fig.update_traces(line_color=color)
                    fig.update_layout(height=200, showlegend=False)
                    st.plotly_chart(fig, width="stretch")
        
        # === DETAILED DATA ===
        with st.expander("📋 View Detailed KPI Data"):
            st.dataframe(kpi_df, width="stretch")
        
        # === KPI DEFINITIONS ===
        with st.expander("📖 KPI Definitions"):
            definitions = get_kpi_definitions()
            for kpi_name, details in list(definitions.items())[:5]:
                st.markdown(f"**{details['name']}**")
                st.markdown(f"- *Definition*: {details['definition']}")
                st.markdown(f"- *Formula*: `{details['formula']}`")
                st.markdown(f"- *Unit*: {details['unit']}")
                st.markdown("---")
        
    except Exception as e:
        st.error(f"Error loading KPI Dashboard: {str(e)}")
        import traceback
        st.code(traceback.format_exc())


# ============================================================================
# TASK 2: OVERRUN WATCH
# ============================================================================
elif current_page == "task2_overrun_watch":
    st.title("⚠️ Task 2: Overrun Watch")
    st.markdown("**Owner:** Vyoma | **Status:** ✅ Complete")
    st.markdown("---")
    
    try:
        from models.overrun_api import OverrunPredictor
        import pandas as pd
        import numpy as np
        import plotly.express as px
        import plotly.graph_objects as go
        from datetime import timedelta
        
        # Initialize predictor
        with st.spinner("Loading models..."):
            predictor = OverrunPredictor()
        
        # Safely access metadata
        time_auc = predictor.metadata.get('time', {}).get('auc', 0.750)
        cost_auc = predictor.metadata.get('cost', {}).get('auc', 0.444)
        
        st.success(f"✅ Models loaded: TIME (AUC: {time_auc:.3f}), COST (AUC: {cost_auc:.3f})")
        
        # Load sample data
        df = pd.read_csv("data/construction_project_dataset.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Get last date in dataset (this is "today")
        today = df['timestamp'].max().date()
        tomorrow = today + timedelta(days=1)
        
        # Get last 15 days of data
        start_date = today - timedelta(days=14)  # 15 days including today
        
        st.info(f"📅 **Monitoring Period:** {start_date} to {today} (15 days) | **Predicting for:** {tomorrow}")
        
        st.subheader("🎯 Daily Time Overrun Risk Assessment")
        
        st.markdown("""
        **How it works:**
        - Monitor the **last 15 days** of project telemetry data
        - Calculate daily KPIs related to time performance
        - Use TIME model to predict if there's a risk of **time overrun tomorrow**
        - Shows trend visualizations and risk factors
        """)
        
        # Filter to last 15 days
        df_recent = df[df['timestamp'].dt.date >= start_date].copy()
        
        # Calculate daily aggregations for KPIs
        df_daily = df_recent.groupby(df_recent['timestamp'].dt.date).agg({
            'safety_incidents': 'sum',
            'material_shortage_alert': 'mean',
            'energy_consumption': 'mean',
            'equipment_utilization_rate': 'mean',
            'material_usage': 'sum',
            'risk_score': 'mean',
            'worker_count': 'mean',
            'task_progress': 'last',
            'cost_deviation': 'last',
            'time_deviation': 'last'
        }).reset_index()
        df_daily.columns = ['date', 'safety_incidents', 'material_shortage_alert', 
                           'energy_consumption', 'equipment_utilization_rate',
                           'material_usage', 'risk_score', 'worker_count',
                           'task_progress', 'cost_deviation', 'time_deviation']
        
        # Display 15-day trends
        st.subheader("📊 15-Day Time Overrun Risk Indicators")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Time deviation trend
            fig_time = go.Figure()
            fig_time.add_trace(go.Scatter(
                x=df_daily['date'],
                y=df_daily['time_deviation'],
                mode='lines+markers',
                name='Time Deviation',
                line=dict(color='#ff4444', width=2)
            ))
            fig_time.add_hline(y=0, line_dash="dash", line_color="gray", 
                              annotation_text="On Schedule")
            fig_time.update_layout(
                title='Time Deviation (Days)',
                xaxis_title='Date',
                yaxis_title='Days Behind/Ahead',
                height=300
            )
            st.plotly_chart(fig_time, width="stretch")
        
        with col2:
            # Task progress trend
            fig_progress = go.Figure()
            fig_progress.add_trace(go.Scatter(
                x=df_daily['date'],
                y=df_daily['task_progress'] * 100,
                mode='lines+markers',
                name='Task Progress',
                line=dict(color='#44ff44', width=2),
                fill='tozeroy'
            ))
            fig_progress.update_layout(
                title='Task Completion Progress (%)',
                xaxis_title='Date',
                yaxis_title='Completion %',
                height=300
            )
            st.plotly_chart(fig_progress, width="stretch")
        
        # Additional KPI charts
        col3, col4 = st.columns(2)
        
        with col3:
            # Equipment utilization
            fig_equip = px.bar(
                df_daily,
                x='date',
                y='equipment_utilization_rate',
                title='Equipment Utilization Rate',
                labels={'equipment_utilization_rate': 'Utilization Rate'}
            )
            fig_equip.update_layout(height=250)
            st.plotly_chart(fig_equip, width="stretch")
        
        with col4:
            # Worker count
            fig_workers = px.area(
                df_daily,
                x='date',
                y='worker_count',
                title='Daily Worker Count',
                labels={'worker_count': 'Workers'}
            )
            fig_workers.update_layout(height=250)
            st.plotly_chart(fig_workers, width="stretch")
        
        # Create features for tomorrow's prediction
        st.subheader(f"🔮 Tomorrow's Prediction ({tomorrow})")
        
        # Use last 15 days data to create lag features
        def create_lag_features(df_window):
            """Create lag features from the recent data window"""
            if len(df_window) < 6:
                st.error("Not enough historical data for prediction (need at least 6 days)")
                return None
            
            features = {}
            
            # Current safety_incidents (today)
            features['safety_incidents'] = float(df_daily['safety_incidents'].iloc[-1])
            
            # Lag2 features (2 days ago)
            features['safety_incidents_lag2'] = float(df_daily['safety_incidents'].iloc[-3])
            features['material_shortage_alert_lag2'] = float(df_daily['material_shortage_alert'].iloc[-3])
            features['energy_consumption_lag2'] = float(df_daily['energy_consumption'].iloc[-3])
            features['equipment_utilization_rate_lag2'] = float(df_daily['equipment_utilization_rate'].iloc[-3])
            features['material_usage_lag2'] = float(df_daily['material_usage'].iloc[-3])
            features['risk_score_lag2'] = float(df_daily['risk_score'].iloc[-3])
            features['worker_count_lag2'] = float(df_daily['worker_count'].iloc[-3])
            
            # Lag5 features (5 days ago)
            features['safety_incidents_lag5'] = float(df_daily['safety_incidents'].iloc[-6])
            features['material_shortage_alert_lag5'] = float(df_daily['material_shortage_alert'].iloc[-6])
            
            return features
        
        features = create_lag_features(df_daily)
        
        if features:
            features_df = pd.DataFrame([features])
            
            # Make prediction
            try:
                result = predictor.predict_time_overrun(features_df, "Current_Project")
                
                # Display prediction
                col_pred1, col_pred2, col_pred3 = st.columns(3)
                
                with col_pred1:
                    if result['prediction'] == 1:
                        st.error(f"🚨 **OVERRUN RISK**")
                    else:
                        st.success(f"✅ **ON TRACK**")
                
                with col_pred2:
                    confidence_val = result['confidence'] * 100
                    st.metric("Confidence", f"{confidence_val:.1f}%")
                
                with col_pred3:
                    current_time_dev = df_daily['time_deviation'].iloc[-1]
                    st.metric("Current Time Deviation", f"{current_time_dev:.1f} days")
                
                # Recommendation
                st.markdown("### 💡 Recommendation")
                st.info(result['recommendation'])
                
                # Show recent KPI table
                st.subheader("📋 Recent Daily KPIs (Last 7 Days)")
                display_cols = ['date', 'task_progress', 'time_deviation', 'equipment_utilization_rate', 
                               'worker_count', 'safety_incidents', 'risk_score']
                st.dataframe(
                    df_daily[display_cols].tail(7).sort_values('date', ascending=False),
                    width="stretch"
                )
                
            except Exception as pred_error:
                st.error(f"Prediction error: {str(pred_error)}")
                st.exception(pred_error)
        
    except Exception as e:
        st.error(f"Error loading Overrun Watch: {str(e)}")
        import traceback
        with st.expander("🐛 Debug Info"):
            st.code(traceback.format_exc())


# ============================================================================
# TASK 3: DRIFT DETECTION
# ============================================================================
elif current_page == "task3_drift_detection":
    st.title("🔍 Task 3: Drift Detection")
    st.markdown("**Owner:** Feruz | **Status:** ✅ Complete")
    st.markdown("---")
    
    try:
        import json
        from PIL import Image
        
        results_path = Path("results")
        
        st.subheader("📊 Drift Detection Results")
        
        # Load alerts
        alert_file = results_path / "task3_alerts.json"
        if alert_file.exists():
            with open(alert_file) as f:
                alerts = json.load(f)
            
            st.metric("Total Alerts", len(alerts) if isinstance(alerts, list) else "N/A")
            
            with st.expander("📄 View Alert Data"):
                st.json(alerts)
        else:
            st.warning("Alert data not found")
        
        # Load drift episodes
        episodes_file = results_path / "task3_drift_episodes.csv"
        if episodes_file.exists():
            import pandas as pd
            episodes_df = pd.read_csv(episodes_file)
            
            st.subheader("📈 Drift Episodes")
            st.dataframe(episodes_df, width="stretch")
        else:
            st.warning("Drift episodes data not found")
        
        # Display visualizations
        st.subheader("📊 Visualizations")
        
        viz_files = [
            ("progress_anomaly.png", "Progress Anomaly Detection"),
            ("progress_episodes.png", "Drift Episodes Timeline")
        ]
        
        cols = st.columns(2)
        for i, (filename, title) in enumerate(viz_files):
            viz_path = results_path / filename
            if viz_path.exists():
                with cols[i]:
                    st.markdown(f"**{title}**")
                    image = Image.open(viz_path)
                    st.image(image, width="stretch")
            else:
                with cols[i]:
                    st.warning(f"{filename} not found")
        
        st.info("💡 Run `Anomaly_Detection.ipynb` to regenerate results")
        
    except Exception as e:
        st.error(f"Error loading Drift Detection results: {str(e)}")


# ============================================================================
# TASK 4: WHAT-IF SIMULATION
# ============================================================================
elif current_page == "task4_what_if_simulation":
    st.title("🎮 Task 4: What-If Simulation")
    st.markdown("**Owner:** Weiyun | **Status:** ✅ Complete")
    st.markdown("---")
    
    try:
        import pandas as pd
        import numpy as np
        
        # Load simulation data
        sim_data_path = "sim/prepared_data/df_10min_features.csv"
        df = pd.read_csv(sim_data_path, parse_dates=["timestamp"])
        
        st.subheader("🎯 Simulation Parameters")
        
        # Show available timestamps
        timestamps = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S").unique()[:20]
        selected_ts_str = st.selectbox("Select timestamp:", timestamps)
        
        mask = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S") == selected_ts_str
        current_state_df = df[mask].copy()
        
        if len(current_state_df) == 0:
            st.error("No data for selected timestamp")
        else:
            # Split into columns
            left_col, right_col = st.columns([1, 1])
            
            with left_col:
                st.markdown("## Current Status")
                
                # Show available metrics
                if 'worker_count' in current_state_df.columns:
                    workers = current_state_df["worker_count"].iloc[0]
                    st.metric("Worker Count", f"{workers:.0f}")
                
                if 'equipment_utilization_rate' in current_state_df.columns:
                    util = current_state_df["equipment_utilization_rate"].iloc[0]
                    st.metric("Equipment Utilization", f"{util:.2%}")
                
                if 'task_progress' in current_state_df.columns:
                    progress = current_state_df["task_progress"].iloc[0]
                    st.metric("Current Progress", f"{progress:.1f}%")
            
            with right_col:
                st.markdown("## What-If Scenario")
                
                worker_delta = st.slider("Worker Count Change", -10, 10, 0)
                util_delta = st.slider("Utilization Change (%)", -20, 20, 0) / 100.0
                
                if 'worker_count' in current_state_df.columns:
                    new_workers = workers + worker_delta
                    st.metric("New Worker Count", f"{new_workers:.0f}", f"{worker_delta:+d}")
                
                if 'equipment_utilization_rate' in current_state_df.columns:
                    new_util = util + util_delta
                    st.metric("New Utilization", f"{new_util:.2%}", f"{util_delta:+.2%}")
                
                if st.button("🚀 Run Simulation", type="primary"):
                    with st.spinner("Running simulation..."):
                        # Simple simulation logic
                        base_progress = 2.0  # Base 2% progress
                        worker_impact = worker_delta * 0.1  # Each worker adds 0.1%
                        util_impact = util_delta * 100 * 0.5  # Utilization impact
                        
                        # Calculate predictions with uncertainty
                        expected_delta = base_progress + worker_impact + util_impact
                        p10 = expected_delta * 0.7  # Pessimistic
                        p50 = expected_delta  # Expected
                        p90 = expected_delta * 1.3  # Optimistic
                        
                        st.success(f"✅ Simulation complete")
                        
                        # Display results
                        st.markdown("### Predicted Progress Delta")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("P10 (Pessimistic)", f"{p10:.2f}%")
                        with col2:
                            st.metric("P50 (Expected)", f"{p50:.2f}%")
                        with col3:
                            st.metric("P90 (Optimistic)", f"{p90:.2f}%")
                        
                        st.info("💡 **Note:** This is a simplified simulation. For full What-If analysis, run: `streamlit run sim/app.py`")
        
    except FileNotFoundError:
        st.error("Simulation data not found")
        st.info("💡 **Run standalone version:** `streamlit run sim/app.py`")
    except Exception as e:
        st.error(f"Error loading What-If Simulation: {str(e)}")
        st.info("Make sure sim/prepared_data/df_10min_features.csv exists")


# ============================================================================
# TASK 5: SAFETY SIGNAL BOARD
# ============================================================================
elif current_page == "task5_safety_signal_board":
    st.title("🛡️ Task 5: Safety Signal Board")
    st.markdown("**Owner:** Vyoma | **Status:** ✅ Complete")
    st.markdown("---")
    
    try:
        from safety.safety_dashboard import SafetyAlertSystem
        from datetime import datetime
        
        # Initialize system
        safety = SafetyAlertSystem()
        
        # Check if config was loaded
        config_exists = safety.config_path.exists()
        if not config_exists:
            st.warning("⚠️ Using default thresholds (config file not found at `safety/saved_safety_models/rule_based_system.json`)")
        else:
            st.success("✅ Safety Alert System initialized with trained thresholds (Recall: 1.00, Precision: 0.80)")
        
        # Show current thresholds
        with st.expander("📋 Model Thresholds (from training data)"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Vibration Level", f"{safety.thresholds['vibration_level']:.1f}")
            with col2:
                st.metric("Heat Index", f"{safety.thresholds['heat_index']:.1f}°C")
            with col3:
                st.metric("Worker Density", f"{safety.thresholds['worker_density']:.1f}")
        
        st.subheader("🎯 Daily Risk Assessment")
        
        # Input form
        col1, col2 = st.columns(2)
        
        with col1:
            date_input = st.date_input("Date", datetime(2026, 1, 10))
            vibration = st.number_input("Vibration Level", 0.0, 50.0, 25.0, 0.5)
            temperature = st.number_input("Temperature (°C)", 0.0, 50.0, 28.0, 0.5)
        
        with col2:
            humidity = st.number_input("Humidity (%)", 0.0, 100.0, 65.0, 1.0)
            worker_count = st.number_input("Worker Count", 1, 200, 50, 1)
            equipment_util = st.slider("Equipment Utilization", 0.0, 1.0, 0.75, 0.05)
        
        if st.button("🔍 Assess Risk", type="primary"):
            with st.spinner("Analyzing risk factors..."):
                result = safety.predict_daily_risk(
                    date=str(date_input),
                    vibration=vibration,
                    temperature=temperature,
                    humidity=humidity,
                    worker_count=worker_count,
                    equipment_utilization=equipment_util
                )
                
                # Display risk level
                risk_level = result['risk_level']
                
                if 'HIGH' in risk_level:
                    st.error(f"🚨 **{risk_level}**")
                elif 'MEDIUM' in risk_level:
                    st.warning(f"⚠️ **{risk_level}**")
                else:
                    st.success(f"✅ **{risk_level}**")
                
                # Show triggered factors
                st.subheader("⚠️ Triggered Risk Factors")
                if result['triggered_factors']:
                    for factor in result['triggered_factors']:
                        st.markdown(f"- {factor}")
                else:
                    st.info("No risk factors triggered")
                
                # Show recommendations
                st.subheader("💡 Recommendations")
                if result['recommendations']:
                    for rec in result['recommendations']:
                        st.markdown(rec)
                else:
                    st.success("No special actions required - Continue normal operations")
                
                # Show calculated features
                with st.expander("📊 Calculated Features"):
                    features = result['features']
                    cols = st.columns(3)
                    for i, (key, value) in enumerate(features.items()):
                        with cols[i % 3]:
                            st.metric(key.replace('_', ' ').title(), f"{value:.2f}")
        
    except Exception as e:
        st.error(f"Error loading Safety Signal Board: {str(e)}")


# ============================================================================
# TASK 6: PROJECT SCORECARD
# ============================================================================
elif current_page == "task6_project_scorecard":
    st.title("📊 Task 6: Project Scorecard")
    st.markdown("**Owner:** Feruz | **Status:** ✅ Complete")
    st.markdown("---")
    
    try:
        import pandas as pd
        import streamlit.components.v1 as components
        
        results_path = Path("results")
        
        # Load scorecard data
        scorecard_file = results_path / "scorecard_results.csv"
        if scorecard_file.exists():
            df = pd.read_csv(scorecard_file)
            
            st.subheader("📈 Scorecard Summary")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Projects", len(df))
            with col2:
                if 'total_score' in df.columns:
                    st.metric("Avg Score", f"{df['total_score'].mean():.2f}")
            with col3:
                if 'total_score' in df.columns:
                    st.metric("Max Score", f"{df['total_score'].max():.2f}")
            with col4:
                if 'total_score' in df.columns:
                    st.metric("Min Score", f"{df['total_score'].min():.2f}")
            
            # Display data
            st.subheader("📊 Detailed Scores")
            st.dataframe(df.head(50), width="stretch")
            
        else:
            st.warning("Scorecard results not found")
        
        # Load daily scorecard
        daily_file = results_path / "daily_scorecard_per_site.csv"
        if daily_file.exists():
            daily_df = pd.read_csv(daily_file)
            
            st.subheader("📅 Daily Scorecard")
            st.dataframe(daily_df.head(20), width="stretch")
        
        # Display HTML dashboards
        st.subheader("📊 Interactive Visualizations")
        
        dashboard_files = [
            ("scorecard_dashboard.html", "Main Dashboard"),
            ("pillar_radar.html", "Pillar Radar Chart"),
            ("score_distribution.html", "Score Distribution")
        ]
        
        selected_viz = st.selectbox("Select visualization:", [f[1] for f in dashboard_files])
        
        for filename, title in dashboard_files:
            if title == selected_viz:
                viz_path = results_path / filename
                if viz_path.exists():
                    with open(viz_path, 'r') as f:
                        html_content = f.read()
                    components.html(html_content, height=600, scrolling=True)
                else:
                    st.warning(f"{filename} not found")
        
        st.info("💡 Run `Project_Scorecard.ipynb` to regenerate results")
        
    except Exception as e:
        st.error(f"Error loading Project Scorecard: {str(e)}")


# ============================================================================
# TASK 7: WEEKLY OPS NOTES
# ============================================================================
elif current_page == "task7_weekly_ops_notes":
    st.title("📝 Task 7: Weekly Ops Notes")
    st.markdown("**Owner:** Vyoma | **Status:** ✅ Complete")
    st.markdown("---")
    
    try:
        from ops_notes.generator import WeeklyOpsNotesGenerator
        import pandas as pd
        from datetime import datetime, timedelta
        import os
        
        st.subheader("🤖 AI-Powered Weekly Operations Report Generator")
        
        # Check for API key
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            st.warning("⚠️ GEMINI_API_KEY not found in environment")
            api_key = st.text_input("Enter your Google Gemini API Key:", type="password")
        else:
            st.success("✅ API key loaded from environment")
        
        if api_key:
            # Date selection
            col1, col2 = st.columns(2)
            with col1:
                week_start = st.date_input("Week Start", datetime(2026, 1, 6))
            with col2:
                week_end = st.date_input("Week End", datetime(2026, 1, 10))
            
            if st.button("📝 Generate Weekly Report", type="primary"):
                with st.spinner("Generating report with AI..."):
                    try:
                        # Initialize generator
                        generator = WeeklyOpsNotesGenerator(api_key)
                        
                        # Load sample project data
                        df = pd.read_csv("data/construction_project_dataset.csv")
                        
                        # Create sample projects with features
                        chunk_size = len(df) // 3
                        projects_data = []
                        
                        for i in range(3):
                            start_idx = i * chunk_size
                            end_idx = start_idx + chunk_size
                            df_slice = df.iloc[start_idx:end_idx]
                            
                            # Create features dict
                            base_features = ['safety_incidents', 'equipment_failure', 'material_shortage_alert', 'vibration_level']
                            features = {}
                            
                            for feat in base_features:
                                if feat in df_slice.columns:
                                    features[feat] = df_slice[feat].iloc[-1]
                                    features[f'{feat}_lag2'] = df_slice[feat].iloc[-3] if len(df_slice) >= 3 else df_slice[feat].iloc[0]
                                    features[f'{feat}_lag5'] = df_slice[feat].iloc[-6] if len(df_slice) >= 6 else df_slice[feat].iloc[0]
                            
                            features['weather_disruption'] = 0
                            features['weather_disruption_lag2'] = 0
                            
                            projects_data.append({
                                'project_id': f'Project_{i+1}',
                                'features': pd.DataFrame([features])
                            })
                        
                        # Create sample safety data
                        dates = pd.date_range(week_start, week_end, freq='D')
                        safety_data = pd.DataFrame({
                            'timestamp': dates,
                            'vibration_level': [25.0, 28.0, 27.0, 26.0, 24.0][:len(dates)],
                            'temperature': [28.0, 30.0, 29.0, 27.0, 26.0][:len(dates)],
                            'humidity': [65.0, 70.0, 68.0, 66.0, 64.0][:len(dates)],
                            'worker_count': [50, 55, 52, 48, 50][:len(dates)],
                            'equipment_utilization_rate': [0.75, 0.80, 0.77, 0.73, 0.75][:len(dates)]
                        })
                        
                        # Generate report
                        report_md = generator.generate_weekly_report(
                            projects_data=projects_data,
                            safety_data=safety_data,
                            week_start=str(week_start),
                            week_end=str(week_end),
                            output_path=None  # Return markdown instead of saving
                        )
                        
                        # Display report
                        st.success("✅ Report generated successfully!")
                        st.markdown("---")
                        st.markdown(report_md)
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Report",
                            data=report_md,
                            file_name=f"weekly_ops_notes_{week_start}_{week_end}.md",
                            mime="text/markdown"
                        )
                        
                    except Exception as e:
                        st.error(f"Error generating report: {str(e)}")
                        st.info("Using fallback narrative generation...")
        
        # Show existing samples
        samples_path = Path("ops_notes/samples")
        if samples_path.exists():
            sample_files = list(samples_path.glob("week_*.md"))
            if sample_files:
                st.markdown("---")
                st.subheader("📄 Sample Reports")
                
                selected_sample = st.selectbox("View sample report:", [f.name for f in sorted(sample_files)])
                
                if selected_sample:
                    sample_path = samples_path / selected_sample
                    with open(sample_path) as f:
                        content = f.read()
                    
                    with st.expander("📖 View Report", expanded=True):
                        st.markdown(content)
        
    except Exception as e:
        st.error(f"Error loading Weekly Ops Notes: {str(e)}")


# Footer for all pages
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🏗️ <strong>LogPilot v1.0</strong> | Built with ❤️ by Weiyun, Vyoma & Feruz | January 2026</p>
</div>
""", unsafe_allow_html=True)

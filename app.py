import streamlit as st
st.set_page_config(layout="wide")

import altair as alt
import pandas as pd
import plotly.graph_objects as go
import time

from kpis.etl_kpis import compute_project_kpis
from sim.what_if import what_if_api

def line_chart_with_limits(df, column, height=250):
    y_min = df[[column]].min().iloc[0] * 0.98
    y_max = df[[column]].max().iloc[0] * 1.02

    chart = (
        alt.Chart(df)
        .mark_line(color='steelblue', point=False)
        .encode(
            x=alt.X('timestamp', title=None),
            y=alt.Y(column, title=None, scale=alt.Scale(domain=[y_min, y_max])),
            tooltip=['timestamp', column]
        )
        .properties(
            height=height,
            width='container',
        )
        .interactive()
    )

    return chart


def render_kpi_dashboard():
    

    freq_option = st.selectbox(
        "📅 Select frequency for KPI calculation:",
        options=["Weekly", "Daily"],
        index=0,
        key="kpi_freq"
    )

    freq_map = {"Weekly": "W", "Daily": "D"}
    freq = freq_map[freq_option]

    df = pd.read_csv("data/construction_project_dataset.csv")
    kpi_df = compute_project_kpis(df, freq=freq)

    # -------- Data Health Index --------
    st.subheader("📊 Data Health Index")
    data_health = kpi_df['data_health_index'].iloc[-1]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=data_health * 100,
        gauge={
            'axis': {'range': [0, 1]},
            'bar': {'color': "#38a538" if data_health >= 0.95 else "#ff7d7d"},
            'steps': [
                {'range': [0, 0.95], 'color': "#ffcccc"},
                {'range': [0.95, 1], 'color': "#ccffcc"}
            ],
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    # -------- Cost & Time --------
    st.subheader("💰 Cost Deviation")
    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(line_chart_with_limits(kpi_df, 'cost_deviation_mean'), use_container_width=True)
    with col2:
        st.altair_chart(line_chart_with_limits(kpi_df, 'cost_deviation_max'), use_container_width=True)

    st.subheader("⏱️ Time Deviation")
    col3, col4 = st.columns(2)
    with col3:
        st.altair_chart(line_chart_with_limits(kpi_df, 'time_deviation_mean'), use_container_width=True)
    with col4:
        st.altair_chart(line_chart_with_limits(kpi_df, 'time_deviation_max'), use_container_width=True)

    st.subheader("🏗️ Equipment Utilization")
    st.altair_chart(
        line_chart_with_limits(kpi_df, 'equipment_utilization_rate_mean', height=300),
        use_container_width=True
    )

    st.subheader("🚀 Task Progress Velocity")
    st.line_chart(kpi_df[['task_progress_last']], height=250)

    st.subheader(f"📋 {freq_option} KPI Summary")
    st.dataframe(kpi_df.tail(10))


@st.cache_data
def load_whatif_data():
    df = pd.read_csv("sim/prepared_data/df_10min_features.csv", parse_dates=["timestamp"])
    df2 = pd.read_csv("data/construction_project_performance_dataset.csv", parse_dates=["Timestamp"])

    merged_df = pd.merge(
        df,
        df2[['Timestamp', 'Optimization_Suggestion']],
        left_on='timestamp',
        right_on='Timestamp',
        how='left'
    ).drop(columns=['Timestamp'], errors='ignore')

    return merged_df


def render_whatif_simulator():
    df = load_whatif_data()

    st.title("⚙️ What-if Simulator")

    selected_ts_str = st.selectbox(
        "Select timestamp",
        df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    )

    mask = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S") == selected_ts_str
    current_state_df = df[mask].copy()

    # Split page into two wide columns
    left_col, right_col = st.columns([1, 1])   # 50% / 50%

    with left_col:
        

        st.markdown("## Current Status")

        st.metric("Current Progress", f"{current_state_df['task_progress'].iloc[0]:.2f}")
        st.markdown("### 📊 Status Overview (last 10 min)")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Risk Score", f"{current_state_df['risk_score'].iloc[0]:.2f}")
        with col2:
            st.metric("Average worker count", f"{int(current_state_df['worker_count'].iloc[0])}")
        with col3:
            st.metric("Avg equipment utilization", f"{current_state_df['equipment_utilization_rate'].iloc[0]:.2f}")

        st.markdown("### 💡 Optimization Suggestion")
        suggestion = current_state_df['Optimization_Suggestion'].iloc[0]
        if pd.notna(suggestion):
            st.info(suggestion)
        else:
            st.caption("No specific suggestions for this timestamp.")

    with right_col:
        st.markdown("## What-if Scenario")

        st.write("Test how adding workers or changing utilization affects **task progress**.")

        # What-If inputs
        min_value = -int(current_state_df['worker_count'].iloc[0]) + 1
        add_workers = st.number_input(f"Add Workers ({min_value} ~ 30)", min_value=min_value, max_value=30, value=2)

        baseline_util = float(current_state_df['equipment_utilization_rate'].iloc[0])
        util_absolute = st.slider(
            "Equipment Utilization (%)",
            min_value=0.0,
            max_value=100.0,
            value=baseline_util,
            step=0.5
        )
        util_change = util_absolute - baseline_util
        st.caption(f"Utilization change: {util_change:+.1f}%")

        st.markdown("### 🔮 Predicted Outcome")

        if st.button("Simulate Scenario"):

            start_time = time.perf_counter()

            output = what_if_api(
                current_state_df=current_state_df, 
                worker_change=add_workers, 
                utilization_change=1 + util_change / 100
            )

            end_time = time.perf_counter()
            response_ms = (end_time - start_time) * 1000  # transform to milliseconds

            current_progress = current_state_df['task_progress'].iloc[0]
            predicted = min(output['progress_delta_estimate'] + current_progress, 100)

            progress_delta = output['progress_delta_estimate']

            st.metric(
                "Predicted Progress (next 10 min)",
                f"{predicted:.2f}",
                delta=f"{progress_delta:+.2f}"
            )
            col3, col4 = st.columns(2)
            with col3:
                st.write(
                    f"90% Uncertainty Band: "
                    f"{output['progress_delta_90_pi'][0] + current_progress:.2f} - "
                    f"{output['progress_delta_90_pi'][1] + current_progress:.2f}"
                )
            with col4:
                st.markdown(f"⏱️ Scenario response time: `{response_ms:.1f} ms`")


st.title("🏗️ Construction Data Dashboard")
tab1, tab2 = st.tabs(["📊 Project KPI Dashboard", "⚙️ What-if Simulator"])

with tab1:
    render_kpi_dashboard()

with tab2:
    render_whatif_simulator()



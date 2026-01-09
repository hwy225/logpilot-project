import altair as alt
import streamlit as st
import pandas as pd
from kpis.etl_kpis import compute_project_kpis
import plotly.graph_objects as go


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

# title
st.title("🏗️ Construction Project KPI Dashboard")

# set frequency option
freq_option = st.selectbox(
    "📅 Select frequency for KPI calculation:",
    options=["Weekly", "Daily"],
    index=0
)

freq_map = {"Weekly": "W", "Daily": "D"}
freq = freq_map[freq_option]

# load data and compute KPIs
df = pd.read_csv("data/construction_project_dataset.csv")
kpi_df = compute_project_kpis(df, freq=freq)

# ===============================
# Data Health Index 
# ===============================
st.subheader("📊 Data Health Index")

data_health = kpi_df['data_health_index'].iloc[-1]

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=data_health*100,
    # title={'text': "Data Health Index"},
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

# ===============================
# Cost & Time Deviation 
# ===============================


st.subheader("💰 Cost Deviation")

col1, col2 = st.columns(2)

with col1:
    st.write("**Average Cost Deviation**")
    chart = line_chart_with_limits(kpi_df, 'cost_deviation_mean', height=250)
    st.altair_chart(chart, use_container_width=True)

with col2:
    st.write("**Max Cost Deviation**")
    chart = line_chart_with_limits(kpi_df, 'cost_deviation_max', height=250)
    st.altair_chart(chart, use_container_width=True)


st.subheader("⏱️ Time Deviation")
col3, col4 = st.columns(2)
with col3:
    st.write("**Average Time Deviation**")
    chart = line_chart_with_limits(kpi_df, 'time_deviation_mean', height=250)
    st.altair_chart(chart, use_container_width=True)

with col4:
    st.write("**Max Time Deviation**")
    chart = line_chart_with_limits(kpi_df, 'time_deviation_max', height=250)
    st.altair_chart(chart, use_container_width=True)

# ===============================
# Equipment Utilization
# ===============================
st.subheader("🏗️ Equipment Utilization")
chart = line_chart_with_limits(kpi_df, 'equipment_utilization_rate_mean', height=300)
st.altair_chart(chart, use_container_width=True)

# ===============================
# Energy / Worker Intensity
# ===============================
st.subheader("⚡ Energy / Worker Intensity")
chart = line_chart_with_limits(kpi_df, 'worker_intensity', height=250)
st.altair_chart(chart, use_container_width=True)

# ===============================
# 🚀 Task Progress Velocity
# ===============================
st.subheader("🚀 Task Progress Velocity")
st.line_chart(kpi_df[['task_progress_last']], height=250)

# ===============================
# 📋 KPI Summary
# ===============================
st.subheader(f"📋 {freq_option} KPI Summary")
st.dataframe(kpi_df.tail(10))

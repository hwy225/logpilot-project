import pandas as pd
import matplotlib.pyplot as plt

# ---- LOAD DATA ----
df1 = pd.read_csv("construction_project_dataset.csv")
df2 = pd.read_csv("construction_project_performance_dataset.csv")

# ---- CLEAN & PREPROCESS ----
df1.columns = [c.strip().lower().replace(' ', '_') for c in df1.columns]
df2.columns = [c.strip().lower().replace(' ', '_') for c in df2.columns]

df1['timestamp'] = pd.to_datetime(df1['timestamp'])
df2['timestamp'] = pd.to_datetime(df2['timestamp'])

# ---- GROUP BY DAY ----
df1_daily = df1.groupby(pd.Grouper(key='timestamp', freq='D')).mean(numeric_only=True).reset_index()
df2_daily = df2.groupby(pd.Grouper(key='timestamp', freq='D')).mean(numeric_only=True).reset_index()

# ---- VISUALIZE ----
plt.style.use('seaborn-v0_8-muted')
plt.figure(figsize=(14, 8))

# === 1. Operational Sensor Trends (Stage 1: Monitoring) ===
plt.subplot(2, 1, 1)
plt.plot(df1_daily['timestamp'], df1_daily['temperature'], label='Temperature (°C)', linewidth=2)
plt.plot(df1_daily['timestamp'], df1_daily['humidity'], label='Humidity (%)', linewidth=2)
plt.plot(df1_daily['timestamp'], df1_daily['vibration_level'], label='Vibration Level', linewidth=2)
plt.title('Stage 1: Daily Operational Sensor Trends — Construction Site Monitoring', fontsize=13)
plt.xlabel('Date')
plt.ylabel('Sensor Values')
plt.legend()
plt.grid(alpha=0.3)

# === 2. Performance & Business Insights (Stage 2: Agentic Evolution) ===
plt.subplot(2, 1, 2)
plt.plot(df1_daily['timestamp'], df1_daily['energy_consumption'], label='Energy Consumption (kWh)', linewidth=2)
plt.plot(df1_daily['timestamp'], df1_daily['cost_deviation'], label='Cost Deviation', linewidth=2)
plt.plot(df1_daily['timestamp'], df1_daily['material_usage'], label='Material Usage (kg)', linewidth=2)
plt.title('Stage 2: Daily Project Performance Insights — Toward Agentic AI', fontsize=13)
plt.xlabel('Date')
plt.ylabel('Aggregated Values')
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("agentic_ai_progress_visualization.png", dpi=300, bbox_inches='tight')
plt.show()
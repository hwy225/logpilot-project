"""
Weekly Ops Notes Generator
===========================
Auto-generates comprehensive weekly operations notes using:
- Task 1: KPI Dashboard (kpis/etl_kpis.py)
- Task 2: Time Overrun API (models/overrun_api.py)
- Task 3: Drift Detection (results/task3_alerts.json)
- Task 4: What-If Simulation results
- Task 5: Safety Alert System (safety/safety_dashboard.py)
- Task 6: Project Scorecard (results/scorecard_results.csv)
- Google Gemini LLM for narrative generation

Author: Logpilot Project Team
Date: January 10, 2026
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import json
import warnings

# Suppress deprecation warning for google.generativeai
warnings.filterwarnings('ignore', category=FutureWarning, module='google.generativeai')

import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from models.overrun_api import OverrunPredictor
from safety.safety_dashboard import SafetyAlertSystem

# Try to import KPI module
try:
    from kpis.etl_kpis import compute_project_kpis
    KPI_AVAILABLE = True
except ImportError:
    KPI_AVAILABLE = False
    print("⚠️  KPI module not available")


class WeeklyOpsNotesGenerator:
    """
    Generate weekly operations notes by combining insights from:
    - Time overrun predictions
    - Safety alert system
    - LLM-powered narrative generation
    """
    
    def __init__(self, gemini_api_key: str):
        """
        Initialize the generator with API connections.
        
        Args:
            gemini_api_key: Google Gemini API key
        """
        print("=" * 80)
        print("INITIALIZING WEEKLY OPS NOTES GENERATOR")
        print("=" * 80)
        
        # Initialize APIs
        self.time_predictor = OverrunPredictor()
        self.safety_system = SafetyAlertSystem()
        
        # Initialize Gemini
        genai.configure(api_key=gemini_api_key)
        # Use the newer model name (gemini-pro is deprecated)
        try:
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except:
            # Fallback to older name if new one not available
            self.model = genai.GenerativeModel('gemini-pro')
        print("✅ Google Gemini configured")
        
        # Load prompt template
        prompt_path = Path(__file__).parent / 'prompt.txt'
        with open(prompt_path, 'r') as f:
            self.prompt_template = f.read()
        print(f"✅ Loaded prompt template: {prompt_path}")
        
        print("=" * 80)
        print("✅ GENERATOR READY")
        print("=" * 80)
    
    def collect_time_overrun_data(
        self, 
        projects_data: List[Dict],
        week_label: str = "Current Week"
    ) -> str:
        """
        Collect time overrun predictions for multiple projects.
        
        Args:
            projects_data: List of dicts with 'features' and 'project_id' (or None to skip)
            week_label: Label for the week being analyzed
            
        Returns:
            Formatted string summary of time overrun predictions
        """
        # Handle None or empty input
        if not projects_data:
            return f"Week: {week_label}\n{'=' * 60}\n\n⚠️  No project data provided - skipping time overrun analysis\n"
        
        print(f"\n📊 Analyzing time overrun risk for {len(projects_data)} projects...")
        
        # Get predictions for all projects
        results = []
        for project in projects_data:
            result = self.time_predictor.predict_time_overrun(
                X=project['features'],
                project_id=project['project_id']
            )
            results.append(result)
        
        # Sort by confidence (highest risk first)
        results_sorted = sorted(results, key=lambda x: x['confidence'], reverse=True)
        
        # Format summary
        summary_lines = [f"Week: {week_label}", "=" * 60, ""]
        
        # Count predictions
        overrun_count = sum(1 for r in results if r['prediction'] == 1)
        no_overrun_count = len(results) - overrun_count
        
        summary_lines.append(f"Total Projects Analyzed: {len(results)}")
        summary_lines.append(f"  - Predicted OVERRUN: {overrun_count}")
        summary_lines.append(f"  - Predicted NO OVERRUN: {no_overrun_count}")
        summary_lines.append("")
        
        if overrun_count > 0:
            summary_lines.append("🚨 HIGH-RISK PROJECTS (Sorted by confidence):")
            summary_lines.append("")
            for i, result in enumerate(results_sorted, 1):
                if result['prediction'] == 1:
                    summary_lines.append(f"{i}. Project: {result['project_id']}")
                    summary_lines.append(f"   Confidence: {result['confidence_pct']}")
                    summary_lines.append(f"   Recommendation: {result['recommendation']}")
                    summary_lines.append("")
        else:
            summary_lines.append("✅ No projects flagged for time overrun this week.")
            summary_lines.append("")
        
        # Add lower-risk projects for context
        if no_overrun_count > 0:
            summary_lines.append("✅ LOWER-RISK PROJECTS:")
            for result in results_sorted:
                if result['prediction'] == 0:
                    summary_lines.append(f"  - {result['project_id']}: {result['confidence_pct']} confidence (NO OVERRUN)")
            summary_lines.append("")
        
        return "\n".join(summary_lines)
    
    def collect_safety_data(
        self, 
        daily_data: pd.DataFrame,
        week_start: str,
        week_end: str
    ) -> str:
        """
        Collect safety alerts for the week.
        
        Args:
            daily_data: DataFrame with columns: date, vibration_level, temperature,
                       humidity, workers_onsite, equipment_count
            week_start: Start date (YYYY-MM-DD)
            week_end: End date (YYYY-MM-DD)
            
        Returns:
            Formatted string summary of safety alerts
        """
        print(f"\n🛡️ Analyzing safety alerts for {week_start} to {week_end}...")
        
        # Filter data for the week
        daily_data['date'] = pd.to_datetime(daily_data['date'])
        week_data = daily_data[
            (daily_data['date'] >= week_start) & 
            (daily_data['date'] <= week_end)
        ].copy()
        
        if len(week_data) == 0:
            return f"Week: {week_start} to {week_end}\nNo data available for this week."
        
        # Get predictions for each day
        predictions = self.safety_system.batch_predict(week_data)
        
        # Count alerts (risk_level is 'HIGH RISK' with space, not 'HIGH_RISK')
        high_risk_days = predictions[predictions['risk_level'] == 'HIGH RISK']
        alert_count = len(high_risk_days)
        
        # Format summary
        summary_lines = [
            f"Week: {week_start} to {week_end}",
            "=" * 60,
            "",
            f"Total Days Monitored: {len(predictions)}",
            f"High-Risk Days: {alert_count}",
            f"Low-Risk Days: {len(predictions) - alert_count}",
            ""
        ]
        
        if alert_count > 0:
            summary_lines.append("🚨 HIGH-RISK DAYS:")
            summary_lines.append("")
            
            for _, row in high_risk_days.iterrows():
                # Handle both string and datetime date formats
                date_str = row['date'] if isinstance(row['date'], str) else row['date'].strftime('%Y-%m-%d')
                summary_lines.append(f"📅 {date_str}")
                summary_lines.append(f"   Risk Level: {row['risk_level']}")
                summary_lines.append(f"   Triggers: {', '.join(row['triggered_factors'])}")
                summary_lines.append(f"   Recommendations:")
                # recommendations is a list, not a string
                recs = row['recommendations'] if isinstance(row['recommendations'], list) else [row['recommendations']]
                for rec in recs:
                    if rec.strip():
                        summary_lines.append(f"     • {rec.strip()}")
                summary_lines.append("")
        else:
            summary_lines.append("✅ No high-risk safety conditions detected this week.")
            summary_lines.append("")
        
        # Add trigger frequency analysis
        if alert_count > 0:
            summary_lines.append("📊 ALERT TRIGGER BREAKDOWN:")
            trigger_counts = {}
            for triggers_list in high_risk_days['triggered_factors']:
                for trigger in triggers_list:
                    # Remove emoji and clean up trigger text
                    clean_trigger = trigger.split(']')[0].replace('[', '').replace('🔧', '').replace('🌡️', '').replace('👷', '').strip()
                    trigger_counts[clean_trigger] = trigger_counts.get(clean_trigger, 0) + 1
            
            for trigger, count in sorted(trigger_counts.items(), key=lambda x: x[1], reverse=True):
                summary_lines.append(f"  - {trigger}: {count} day(s)")
            summary_lines.append("")
        
        return "\n".join(summary_lines)
    
    def collect_kpi_data(
        self,
        df: pd.DataFrame,
        week_start: str,
        week_end: str
    ) -> str:
        """
        Collect KPI dashboard data (Task 1).
        
        Args:
            df: DataFrame with project telemetry data
            week_start: Start date (YYYY-MM-DD)
            week_end: End date (YYYY-MM-DD)
            
        Returns:
            Formatted string summary of key KPIs
        """
        if not KPI_AVAILABLE:
            return "KPI module not available - skipping KPI analysis."
        
        print(f"\n📊 Analyzing KPIs for {week_start} to {week_end}...")
        
        try:
            # Compute weekly KPIs
            kpis = compute_project_kpis(df, freq='W')
            
            # Filter to current week
            kpis['date'] = pd.to_datetime(kpis['date'])
            week_kpis = kpis[
                (kpis['date'] >= week_start) & 
                (kpis['date'] <= week_end)
            ]
            
            if len(week_kpis) == 0:
                return f"No KPI data available for {week_start} to {week_end}"
            
            # Get latest values
            latest = week_kpis.iloc[-1]
            
            summary_lines = [
                f"Week: {week_start} to {week_end}",
                "=" * 60,
                "",
                "📈 KEY PERFORMANCE INDICATORS:",
                "",
                f"Cost Performance:",
                f"  - Cost Deviation: {latest.get('cost_deviation_mean', 0):.2f}",
                f"  - Trend: {'⬆️ Increasing' if latest.get('cost_deviation_mean', 0) > 0 else '⬇️ Decreasing'}",
                "",
                f"Schedule Performance:",
                f"  - Time Deviation: {latest.get('time_deviation_mean', 0):.2f} days",
                f"  - Task Progress: {latest.get('task_progress_last', 0):.1%}",
                f"  - Progress Velocity: {latest.get('progress_velocity', 0):.2f}",
                "",
                f"Resource Utilization:",
                f"  - Equipment Utilization: {latest.get('equipment_utilization_rate_mean', 0):.1%}",
                f"  - Worker Intensity: {latest.get('worker_intensity', 0):.2f}",
                "",
                f"Data Health:",
                f"  - Data Health Index: {latest.get('data_health_index', 0):.1f}/100",
                f"  - Status: {'✅ Healthy' if latest.get('data_health_index', 0) >= 95 else '⚠️ Needs Attention'}",
                ""
            ]
            
            return "\n".join(summary_lines)
            
        except Exception as e:
            return f"Error collecting KPI data: {str(e)}"
    
    def collect_drift_data(
        self,
        week_start: str,
        week_end: str
    ) -> str:
        """
        Collect drift detection alerts (Task 3).
        
        Args:
            week_start: Start date (YYYY-MM-DD)
            week_end: End date (YYYY-MM-DD)
            
        Returns:
            Formatted string summary of drift alerts
        """
        print(f"\n🔍 Analyzing drift alerts for {week_start} to {week_end}...")
        
        alerts_path = Path("results/task3_alerts.json")
        episodes_path = Path("results/task3_drift_episodes.csv")
        
        if not alerts_path.exists():
            return f"No drift detection data available (file not found: {alerts_path})"
        
        try:
            # Load alerts
            with open(alerts_path, 'r') as f:
                alerts = json.load(f)
            
            # Filter alerts for this week
            week_alerts = []
            start_dt = pd.to_datetime(week_start)
            end_dt = pd.to_datetime(week_end)
            
            for alert in alerts:
                # Task 3 alerts have 'start_time' and 'end_time', not 'timestamp' or 'date'
                alert_start = pd.to_datetime(alert.get('start_time', alert.get('timestamp', alert.get('date', ''))))
                alert_end = pd.to_datetime(alert.get('end_time', alert_start))
                
                # Include if alert overlaps with our week
                if (alert_start <= end_dt) and (alert_end >= start_dt):
                    week_alerts.append(alert)
            
            summary_lines = [
                f"Week: {week_start} to {week_end}",
                "=" * 60,
                "",
                f"Total Anomalies Detected: {len(week_alerts)}",
                ""
            ]
            
            if len(week_alerts) > 0:
                summary_lines.append("🚨 DETECTED ANOMALIES:")
                summary_lines.append("")
                
                for i, alert in enumerate(week_alerts[:10], 1):  # Show first 10
                    summary_lines.append(f"{i}. Episode {alert.get('episode_id', 'N/A')}: {alert.get('start_time', 'Unknown')} to {alert.get('end_time', 'Unknown')}")
                    summary_lines.append(f"   Severity: {alert.get('severity', 'Unknown')}")
                    summary_lines.append(f"   Duration: {alert.get('duration_hours', 0):.1f} hours")
                    summary_lines.append(f"   Impact Score: {alert.get('impact_score', 0):.2f}")
                    summary_lines.append(f"   Reason: {alert.get('reason', 'N/A')}")
                    summary_lines.append(f"   Action: {alert.get('recommended_action', 'N/A')}")
                    summary_lines.append("")
                
                if len(week_alerts) > 10:
                    summary_lines.append(f"... and {len(week_alerts) - 10} more anomalies")
                    summary_lines.append("")
            else:
                summary_lines.append("✅ No anomalies detected this week - operations normal.")
                summary_lines.append("")
            
            return "\n".join(summary_lines)
            
        except Exception as e:
            return f"Error collecting drift data: {str(e)}"
    
    def collect_scorecard_data(
        self,
        week_start: str,
        week_end: str
    ) -> str:
        """
        Collect project scorecard data (Task 6).
        
        Args:
            week_start: Start date (YYYY-MM-DD)
            week_end: End date (YYYY-MM-DD)
            
        Returns:
            Formatted string summary of scorecard metrics
        """
        print(f"\n📊 Analyzing project scorecard for {week_start} to {week_end}...")
        
        scorecard_path = Path("results/scorecard_results.csv")
        daily_path = Path("results/daily_scorecard_per_site.csv")
        
        if not scorecard_path.exists() and not daily_path.exists():
            return "No scorecard data available"
        
        try:
            summary_lines = [
                f"Week: {week_start} to {week_end}",
                "=" * 60,
                ""
            ]
            
            # Try daily scorecard first (Task 6 output)
            if daily_path.exists():
                df = pd.read_csv(daily_path)
                
                # Task 6 uses 'Date' (capital D) and 'Sensor_ID'
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'])
                    # Filter to week
                    week_df = df[(df['Date'] >= week_start) & (df['Date'] <= week_end)]
                    
                    if len(week_df) == 0:
                        summary_lines.append(f"No scorecard data available for this week.")
                        summary_lines.append(f"(Data available: {df['Date'].min()} to {df['Date'].max()})")
                        summary_lines.append("")
                        return "\n".join(summary_lines)
                    
                    # Task 6 columns: Composite_Score, Traffic_Light, Schedule/Cost/Utilization/Safety/Risk_Normalized
                    if 'Composite_Score' in week_df.columns:
                        avg_score = week_df['Composite_Score'].mean()
                        max_score = week_df['Composite_Score'].max()
                        min_score = week_df['Composite_Score'].min()
                        
                        # Count traffic lights
                        if 'Traffic_Light' in week_df.columns:
                            lights = week_df['Traffic_Light'].value_counts().to_dict()
                            green = lights.get('Green', 0)
                            yellow = lights.get('Yellow', 0)
                            red = lights.get('Red', 0)
                        else:
                            green = yellow = red = 0
                        
                        summary_lines.extend([
                            "📈 PROJECT HEALTH SCORES:",
                            "",
                            f"  Average Composite Score: {avg_score:.2f}/100",
                            f"  Best Daily Performance: {max_score:.2f}/100",
                            f"  Lowest Daily Performance: {min_score:.2f}/100",
                            "",
                            "🚦 TRAFFIC LIGHT DISTRIBUTION:",
                            f"  🟢 Green (Good): {green} day(s)",
                            f"  🟡 Yellow (Caution): {yellow} day(s)",
                            f"  🔴 Red (Critical): {red} day(s)",
                            "",
                            f"  Overall Health: {'✅ Good' if avg_score >= 80 else '⚠️ Concerning' if avg_score >= 60 else '🚨 Critical'}",
                            ""
                        ])
                        
                        # Show sensor/site breakdown if multiple
                        if 'Sensor_ID' in week_df.columns and week_df['Sensor_ID'].nunique() > 1:
                            sensor_avgs = week_df.groupby('Sensor_ID')['Composite_Score'].mean().sort_values(ascending=False)
                            summary_lines.append("📍 SITE/SENSOR PERFORMANCE:")
                            for sensor, score in sensor_avgs.head(5).items():
                                summary_lines.append(f"  {sensor}: {score:.2f}/100")
                            summary_lines.append("")
            
            # Fallback to scorecard_results.csv if exists
            elif scorecard_path.exists():
                df = pd.read_csv(scorecard_path)
                
                if 'total_score' in df.columns:
                    avg_score = df['total_score'].mean()
                    max_score = df['total_score'].max()
                    min_score = df['total_score'].min()
                    
                    summary_lines.extend([
                        "📈 PROJECT HEALTH SCORES:",
                        "",
                        f"  Average Score: {avg_score:.2f}/100",
                        f"  Best Performer: {max_score:.2f}/100",
                        f"  Needs Attention: {min_score:.2f}/100",
                        f"  Health Status: {'✅ Good' if avg_score >= 70 else '⚠️ Concerning' if avg_score >= 50 else '🚨 Critical'}",
                        ""
                    ])
                    
                    # Identify top and bottom performers
                    if len(df) > 0:
                        if 'project_id' in df.columns or 'site_id' in df.columns:
                            id_col = 'project_id' if 'project_id' in df.columns else 'site_id'
                            top_project = df.loc[df['total_score'].idxmax()]
                            bottom_project = df.loc[df['total_score'].idxmin()]
                            
                            summary_lines.extend([
                                f"🏆 Top Performer: {top_project.get(id_col, 'Unknown')} ({top_project['total_score']:.2f})",
                                f"⚠️  Needs Support: {bottom_project.get(id_col, 'Unknown')} ({bottom_project['total_score']:.2f})",
                                ""
                            ])
            else:
                summary_lines.append("Project scorecard summary not available")
                summary_lines.append("")
            
            return "\n".join(summary_lines)
            
        except Exception as e:
            return f"Error collecting scorecard data: {str(e)}"
    
    def generate_narrative(
        self,
        time_overrun_summary: str,
        safety_summary: str,
        kpi_summary: str = "",
        drift_summary: str = "",
        scorecard_summary: str = ""
    ) -> str:
        """
        Generate narrative ops notes using LLM.
        
        Args:
            time_overrun_summary: Formatted time overrun data
            safety_summary: Formatted safety alert data
            kpi_summary: Formatted KPI data (Task 1)
            drift_summary: Formatted drift detection data (Task 3)
            scorecard_summary: Formatted scorecard data (Task 6)
            
        Returns:
            LLM-generated weekly ops notes
        """
        print("\n🤖 Generating narrative with Google Gemini...")
        
        # Fill prompt template with all available data
        prompt = self.prompt_template.format(
            kpi_data=kpi_summary or "No KPI data available",
            time_overrun_data=time_overrun_summary,
            drift_data=drift_summary or "No drift detection data available",
            safety_data=safety_summary,
            scorecard_data=scorecard_summary or "No scorecard data available"
        )
        
        # Generate with Gemini
        try:
            response = self.model.generate_content(prompt)
            narrative = response.text
            print("✅ Narrative generated successfully")
            return narrative
        except Exception as e:
            print(f"❌ Error generating narrative: {e}")
            # Return fallback template
            return self._generate_fallback_narrative(
                time_overrun_summary, safety_summary, kpi_summary, 
                drift_summary, scorecard_summary
            )
    
    def _generate_fallback_narrative(
        self,
        time_overrun_summary: str,
        safety_summary: str,
        kpi_summary: str = "",
        drift_summary: str = "",
        scorecard_summary: str = ""
    ) -> str:
        """
        Generate basic narrative without LLM (fallback).
        """
        sections = []
        
        if kpi_summary:
            sections.append(f"### KPI Dashboard\n```\n{kpi_summary}\n```\n")
        
        sections.append(f"### Time Overrun Predictions\n```\n{time_overrun_summary}\n```\n")
        
        if drift_summary:
            sections.append(f"### Drift Detection\n```\n{drift_summary}\n```\n")
        
        sections.append(f"### Safety Alerts\n```\n{safety_summary}\n```\n")
        
        if scorecard_summary:
            sections.append(f"### Project Scorecard\n```\n{scorecard_summary}\n```\n")
        
        return f"""# Weekly Operations Summary

## Raw Data

{chr(10).join(sections)}

## Note
Full narrative generation unavailable. Please review raw data above.
"""
    
    def generate_weekly_report(
        self,
        projects_data: List[Dict],
        safety_data: pd.DataFrame,
        telemetry_data: Optional[pd.DataFrame],
        week_start: str,
        week_end: str,
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate complete weekly ops notes report integrating all monitoring systems.
        
        Args:
            projects_data: List of projects with features for overrun prediction
            safety_data: DataFrame with daily safety metrics
            telemetry_data: DataFrame with project telemetry for KPIs (optional)
            week_start: Start date (YYYY-MM-DD)
            week_end: End date (YYYY-MM-DD)
            output_path: Optional path to save report
            
        Returns:
            Complete weekly ops notes (markdown format)
        """
        print("\n" + "=" * 80)
        print(f"GENERATING COMPREHENSIVE WEEKLY OPS NOTES: {week_start} to {week_end}")
        print("=" * 80)
        
        # Collect data from all monitoring systems
        
        # Task 1: KPI Dashboard
        kpi_summary = ""
        if telemetry_data is not None:
            kpi_summary = self.collect_kpi_data(telemetry_data, week_start, week_end)
        else:
            print("⚠️  No telemetry data provided - skipping KPI analysis")
        
        # Task 2: Time Overrun Predictions
        time_summary = self.collect_time_overrun_data(
            projects_data, 
            week_label=f"{week_start} to {week_end}"
        )
        
        # Task 3: Drift Detection
        drift_summary = self.collect_drift_data(week_start, week_end)
        
        # Task 5: Safety Alerts
        safety_summary = self.collect_safety_data(
            safety_data,
            week_start,
            week_end
        )
        
        # Task 6: Project Scorecard
        scorecard_summary = self.collect_scorecard_data(week_start, week_end)
        
        # Generate narrative with LLM
        narrative = self.generate_narrative(
            time_summary, safety_summary, kpi_summary, 
            drift_summary, scorecard_summary
        )
        
        # Build comprehensive report
        report = f"""# Comprehensive Weekly Operations Report
**Period**: {week_start} to {week_end}  
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Data Sources**: All 7 Logpilot Monitoring Systems

---

{narrative}

---

## Raw Data Appendix

### Task 1: KPI Dashboard
```
{kpi_summary if kpi_summary else "No KPI data available"}
```

### Task 2: Time Overrun Predictions
```
{time_summary}
```

### Task 3: Drift Detection Alerts
```
{drift_summary}
```

### Task 5: Safety Alert Analysis
```
{safety_summary}
```

### Task 6: Project Scorecard
```
{scorecard_summary}
```

---
*Generated by Logpilot AI Operations Assistant*  
*Integrating data from: KPI Dashboard • Overrun Predictor • Drift Detection • Safety Alerts • Project Scorecard*
"""
        
        # Save if path provided
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"\n✅ Report saved to: {output_file}")
        
        print("\n" + "=" * 80)
        print("✅ COMPREHENSIVE WEEKLY OPS NOTES GENERATION COMPLETE")
        print("=" * 80)
        
        return report


def main_example():
    """
    Example usage of the Weekly Ops Notes Generator.
    """
    # Get API key from environment
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not set in environment")
        print("Please set it with: export GEMINI_API_KEY='your-api-key'")
        return
    
    # Initialize generator
    generator = WeeklyOpsNotesGenerator(gemini_api_key=api_key)
    
    # Example: Prepare sample project data for time overrun
    # NOTE: In this demo, we pass None to skip time overrun predictions
    # since the TIME model requires complex lag features from historical data.
    # In production, you would pass real project data with all required features:
    # - safety_incidents, safety_incidents_lag2, safety_incidents_lag5
    # - material_shortage_alert_lag2, material_shortage_alert_lag5
    # - worker_count_lag2, material_usage_lag2
    # - equipment_utilization_rate_lag2, energy_consumption_lag2
    # - risk_score_lag2
    # See test_api.py for examples of how to prepare complete feature sets.
    projects_data = None  # Set to list of dicts with project features in production
    
    # Example: Prepare sample safety data for the week
    # Using dates where ALL data sources have data: 2023-01-01 to 2023-01-07
    # - Main dataset: 2023-01-01 to 2023-02-04 ✅
    # - Scorecard: 2023-01-01 to 2023-01-07 ✅
    # - Drift alerts: 2023-01-01 ✅
    safety_data = pd.DataFrame({
        'date': pd.date_range('2023-01-01', '2023-01-07', freq='D'),
        'timestamp': pd.date_range('2023-01-01', '2023-01-07', freq='D'),  # batch_predict needs this
        'vibration_level': [45.3, 38.3, 24.1, 26.7, 23.9, 39.8, 28.2],  # Day 1, 2, 6 above threshold
        'temperature': [35, 31, 29, 32, 30, 33, 29],
        'humidity': [78, 70, 68, 72, 69, 75, 67],
        'worker_count': [65, 52, 48, 55, 50, 58, 46],
        'equipment_count': [12, 10, 9, 11, 9, 12, 8],
        'equipment_utilization_rate': [0.85, 0.8, 0.75, 0.85, 0.72, 0.88, 0.74]  # batch_predict needs this
    })
    
    # Example: Prepare telemetry data for KPI analysis
    # (In production, this would come from your sensors/database)
    # For demo, we'll pass None to skip KPI analysis
    telemetry_data = None  # Set to DataFrame with project telemetry if available
    
    # Generate report for FIRST WEEK (has all data sources)
    report = generator.generate_weekly_report(
        projects_data=projects_data,
        safety_data=safety_data,
        telemetry_data=telemetry_data,
        week_start='2023-01-01',  # First week with complete data
        week_end='2023-01-07',    # Scorecard data ends here
        output_path='ops_notes/samples/week_2023_01_01.md'
    )
    
    print("\n" + "=" * 80)
    print("PREVIEW OF GENERATED REPORT:")
    print("=" * 80)
    print(report[:500] + "...\n")


if __name__ == "__main__":
    main_example()

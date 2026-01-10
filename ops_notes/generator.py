"""
Weekly Ops Notes Generator
===========================
Auto-generates weekly operations notes using:
- Time Overrun API (models/overrun_api.py)
- Safety Alert System (safety/safety_dashboard.py)
- Google Gemini LLM for narrative generation

Author: Logpilot Project Team
Date: January 9, 2026
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
            projects_data: List of dicts with 'features' and 'project_id'
            week_label: Label for the week being analyzed
            
        Returns:
            Formatted string summary of time overrun predictions
        """
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
        
        # Count alerts
        high_risk_days = predictions[predictions['risk_level'] == 'HIGH_RISK']
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
                summary_lines.append(f"📅 {row['date'].strftime('%Y-%m-%d (%A)')}")
                summary_lines.append(f"   Risk Level: {row['risk_level']}")
                summary_lines.append(f"   Triggers: {row['triggers']}")
                summary_lines.append(f"   Recommendations:")
                for rec in row['recommendations'].split('\n'):
                    if rec.strip():
                        summary_lines.append(f"     {rec.strip()}")
                summary_lines.append("")
        else:
            summary_lines.append("✅ No high-risk safety conditions detected this week.")
            summary_lines.append("")
        
        # Add trigger frequency analysis
        if alert_count > 0:
            summary_lines.append("📊 ALERT TRIGGER BREAKDOWN:")
            trigger_counts = {}
            for triggers in high_risk_days['triggers']:
                for trigger in triggers.split(', '):
                    trigger_counts[trigger] = trigger_counts.get(trigger, 0) + 1
            
            for trigger, count in sorted(trigger_counts.items(), key=lambda x: x[1], reverse=True):
                summary_lines.append(f"  - {trigger}: {count} day(s)")
            summary_lines.append("")
        
        return "\n".join(summary_lines)
    
    def generate_narrative(
        self,
        time_overrun_summary: str,
        safety_summary: str
    ) -> str:
        """
        Generate narrative ops notes using LLM.
        
        Args:
            time_overrun_summary: Formatted time overrun data
            safety_summary: Formatted safety alert data
            
        Returns:
            LLM-generated weekly ops notes
        """
        print("\n🤖 Generating narrative with Google Gemini...")
        
        # Fill prompt template
        prompt = self.prompt_template.format(
            time_overrun_data=time_overrun_summary,
            safety_data=safety_summary
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
            return self._generate_fallback_narrative(time_overrun_summary, safety_summary)
    
    def _generate_fallback_narrative(
        self,
        time_overrun_summary: str,
        safety_summary: str
    ) -> str:
        """
        Generate basic narrative without LLM (fallback).
        """
        return f"""# Weekly Operations Summary

## Raw Data

### Time Overrun Predictions
```
{time_overrun_summary}
```

### Safety Alerts
```
{safety_summary}
```

## Note
Full narrative generation unavailable. Please review raw data above.
"""
    
    def generate_weekly_report(
        self,
        projects_data: List[Dict],
        safety_data: pd.DataFrame,
        week_start: str,
        week_end: str,
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate complete weekly ops notes report.
        
        Args:
            projects_data: List of projects with features
            safety_data: DataFrame with daily safety metrics
            week_start: Start date (YYYY-MM-DD)
            week_end: End date (YYYY-MM-DD)
            output_path: Optional path to save report
            
        Returns:
            Complete weekly ops notes (markdown format)
        """
        print("\n" + "=" * 80)
        print(f"GENERATING WEEKLY OPS NOTES: {week_start} to {week_end}")
        print("=" * 80)
        
        # Collect data from both systems
        time_summary = self.collect_time_overrun_data(
            projects_data, 
            week_label=f"{week_start} to {week_end}"
        )
        
        safety_summary = self.collect_safety_data(
            safety_data,
            week_start,
            week_end
        )
        
        # Generate narrative
        narrative = self.generate_narrative(time_summary, safety_summary)
        
        # Add header and metadata
        report = f"""# Weekly Operations Report
**Period**: {week_start} to {week_end}  
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Systems**: Time Overrun Predictor + Safety Alert System

---

{narrative}

---

## Raw Data Appendix

### Time Overrun Analysis
```
{time_summary}
```

### Safety Alert Analysis
```
{safety_summary}
```

---
*Generated by Logpilot AI Operations Assistant*
"""
        
        # Save if path provided
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"\n✅ Report saved to: {output_file}")
        
        print("\n" + "=" * 80)
        print("✅ WEEKLY OPS NOTES GENERATION COMPLETE")
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
    # (In production, this would come from your database)
    projects_data = [
        {
            'project_id': 'Alpha_Tower',
            'features': {
                'project_complexity': 8.5,
                'weather_conditions': 6.2,
                'material_availability': 7.1,
                'labor_productivity': 5.8,
                # Add other required features...
            }
        },
        {
            'project_id': 'Beta_Bridge',
            'features': {
                'project_complexity': 6.5,
                'weather_conditions': 7.5,
                'material_availability': 8.2,
                'labor_productivity': 7.9,
                # Add other required features...
            }
        }
    ]
    
    # Example: Prepare sample safety data for the week
    # (In production, this would come from your sensors/database)
    safety_data = pd.DataFrame({
        'date': pd.date_range('2026-01-06', '2026-01-10', freq='D'),
        'vibration_level': [22.5, 28.3, 24.1, 26.7, 23.9],
        'temperature': [28, 31, 29, 32, 30],
        'humidity': [65, 70, 68, 72, 69],
        'workers_onsite': [45, 52, 48, 55, 50],
        'equipment_count': [8, 10, 9, 11, 9]
    })
    
    # Generate report
    report = generator.generate_weekly_report(
        projects_data=projects_data,
        safety_data=safety_data,
        week_start='2026-01-06',
        week_end='2026-01-10',
        output_path='ops_notes/samples/week_2026_01_06.md'
    )
    
    print("\n" + "=" * 80)
    print("PREVIEW OF GENERATED REPORT:")
    print("=" * 80)
    print(report[:500] + "...\n")


if __name__ == "__main__":
    main_example()

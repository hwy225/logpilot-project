"""
Safety Leading Indicators Dashboard
====================================

Rule-based early warning system for construction site safety.
Predicts daily risk level using vibration, heat index, and worker density.

Author: Safety Analytics Team
Date: December 16, 2025
Version: 1.0
"""

import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from pathlib import Path


class SafetyAlertSystem:
    """
    Rule-based safety alert system for construction sites.
    
    Uses three leading indicators:
    1. Vibration level (machinery operation intensity)
    2. Heat index (temperature + humidity combined)
    3. Worker density (congestion metric)
    
    Alert triggers if ANY threshold exceeded (OR logic).
    """
    
    def __init__(self, config_path: str = "safety/saved_safety_models/rule_based_system.json"):
        """
        Initialize the safety alert system.
        
        Args:
            config_path: Path to JSON file with thresholds and parameters
        """
        self.config_path = Path(config_path)
        self.load_thresholds()
        
    def load_thresholds(self):
        """Load thresholds from configuration file."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                self.thresholds = config['thresholds']
                self.performance = config.get('validation_performance', {})
        else:
            # Default thresholds if config not found (more realistic values)
            self.thresholds = {
                'vibration_level': 35.0,      # Raised from 25.16
                'heat_index': 35.0,            # Raised from 30.0
                'worker_density': 100.0        # Raised from 0.36 (was causing issues)
            }
            self.performance = {}
    
    def calculate_heat_index(self, temperature: float, humidity: float) -> float:
        """
        Calculate heat index from temperature and humidity.
        
        Args:
            temperature: Temperature in Celsius
            humidity: Relative humidity in percentage (0-100)
            
        Returns:
            heat_index: Combined heat stress indicator
        """
        heat_index = temperature + 0.5555 * (humidity / 100) * (temperature - 14.0)
        return heat_index
    
    def calculate_worker_density(self, worker_count: float, 
                                 equipment_utilization: float) -> float:
        """
        Calculate worker density (congestion indicator).
        
        Args:
            worker_count: Number of workers on site
            equipment_utilization: Equipment utilization rate (0-1)
            
        Returns:
            worker_density: Workers per equipment unit
        """
        worker_density = worker_count / (equipment_utilization + 0.1)
        return worker_density
    
    def check_thresholds(self, vibration: float, heat_index: float, 
                        worker_density: float) -> Tuple[str, List[str], List[str]]:
        """
        Check if any threshold is exceeded and generate alerts.
        
        Args:
            vibration: Average vibration level
            heat_index: Calculated heat index (°C)
            worker_density: Calculated worker density
            
        Returns:
            risk_level: 'HIGH RISK' or 'LOW RISK'
            triggered_factors: List of factors that triggered alert
            recommendations: List of safety recommendations
        """
        triggered = []
        recommendations = []
        
        # Check vibration threshold
        if vibration > self.thresholds['vibration_level']:
            triggered.append(
                f"🔧 Vibration ({vibration:.1f} > {self.thresholds['vibration_level']:.1f})"
            )
            recommendations.append(
                "• Inspect all machinery before operation\n"
                "• Reduce concurrent heavy equipment usage\n"
                "• Increase operator breaks (every 2 hours)\n"
                "• Mandatory vibration PPE checks"
            )
        
        # Check heat index threshold
        if heat_index > self.thresholds['heat_index']:
            triggered.append(
                f"🌡️  Heat Index ({heat_index:.1f}°C > {self.thresholds['heat_index']:.1f}°C)"
            )
            recommendations.append(
                "• Mandatory hydration breaks every hour\n"
                "• Shift work to cooler hours (avoid 12-4 PM)\n"
                "• Deploy cooling stations with water and shade\n"
                "• Enforce heat-appropriate PPE"
            )
        
        # Check worker density threshold
        if worker_density > self.thresholds['worker_density']:
            triggered.append(
                f"👷 Worker Density ({worker_density:.2f} > {self.thresholds['worker_density']:.2f})"
            )
            recommendations.append(
                "• Stagger work schedules to reduce congestion\n"
                "• Expand work zones (increase spacing)\n"
                "• Deploy additional supervisors\n"
                "• Implement one-way traffic rules"
            )
        
        risk_level = 'HIGH RISK' if len(triggered) > 0 else 'LOW RISK'
        
        return risk_level, triggered, recommendations
    
    def predict_daily_risk(self, date: str, vibration: float, temperature: float,
                          humidity: float, worker_count: float, 
                          equipment_utilization: float) -> Dict:
        """
        Main prediction function for daily risk assessment.
        
        Args:
            date: Date string (YYYY-MM-DD)
            vibration: Average vibration level for the day
            temperature: Average temperature (°C)
            humidity: Average humidity (%)
            worker_count: Average worker count
            equipment_utilization: Average equipment utilization rate (0-1)
            
        Returns:
            Dict with risk assessment, triggers, and recommendations
        """
        # Calculate derived features
        heat_index = self.calculate_heat_index(temperature, humidity)
        worker_density = self.calculate_worker_density(worker_count, equipment_utilization)
        
        # Check thresholds
        risk_level, triggers, recommendations = self.check_thresholds(
            vibration, heat_index, worker_density
        )
        
        # Build response
        result = {
            'date': date,
            'risk_level': risk_level,
            'features': {
                'vibration_level': round(vibration, 2),
                'heat_index': round(heat_index, 2),
                'worker_density': round(worker_density, 2),
                'temperature': round(temperature, 2),
                'humidity': round(humidity, 2),
                'worker_count': round(worker_count, 1),
                'equipment_utilization': round(equipment_utilization, 3)
            },
            'thresholds': self.thresholds,
            'triggered_factors': triggers,
            'recommendations': recommendations,
            'system_performance': self.performance,
            'timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def batch_predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Predict risk for multiple days from DataFrame.
        
        Args:
            data: DataFrame with columns: 
                  ['timestamp', 'vibration_level', 'temperature', 
                   'humidity', 'worker_count', 'equipment_utilization_rate']
                   
        Returns:
            DataFrame with predictions added
        """
        results = []
        
        for _, row in data.iterrows():
            result = self.predict_daily_risk(
                date=str(row['timestamp'].date()) if 'timestamp' in row else 'N/A',
                vibration=row['vibration_level'],
                temperature=row['temperature'],
                humidity=row['humidity'],
                worker_count=row['worker_count'],
                equipment_utilization=row.get('equipment_utilization_rate', 
                                             row.get('equipment_utilization', 0.5))
            )
            results.append(result)
        
        # Convert to DataFrame
        predictions_df = pd.DataFrame(results)
        return predictions_df
    
    def generate_alert_report(self, prediction: Dict) -> str:
        """
        Generate formatted alert report for printing/email.
        
        Args:
            prediction: Result dictionary from predict_daily_risk()
            
        Returns:
            Formatted string report
        """
        report = []
        report.append("=" * 70)
        report.append("🚨 CONSTRUCTION SITE SAFETY ALERT")
        report.append("=" * 70)
        report.append(f"\n📅 Date: {prediction['date']}")
        report.append(f"⏰ Generated: {prediction['timestamp']}")
        
        report.append(f"\n🎯 RISK ASSESSMENT: {prediction['risk_level']}")
        
        if prediction['risk_level'] == 'HIGH RISK':
            report.append("\n" + "⚠️  " * 10)
            report.append("\n⚠️  ALERT TRIGGERS:")
            for trigger in prediction['triggered_factors']:
                report.append(f"    {trigger}")
            
            report.append("\n📋 REQUIRED ACTIONS:")
            for i, rec in enumerate(prediction['recommendations'], 1):
                report.append(f"\n  {i}. {rec}")
            
            report.append("\n" + "⚠️  " * 10)
        else:
            report.append("\n✅ No elevated risk factors detected.")
            report.append("   Standard safety protocols apply.")
        
        report.append("\n\n📊 MEASURED VALUES:")
        features = prediction['features']
        report.append(f"    Vibration Level:   {features['vibration_level']:.2f}")
        report.append(f"    Heat Index:        {features['heat_index']:.2f}°C")
        report.append(f"    Worker Density:    {features['worker_density']:.2f}")
        report.append(f"    Temperature:       {features['temperature']:.2f}°C")
        report.append(f"    Humidity:          {features['humidity']:.1f}%")
        report.append(f"    Worker Count:      {features['worker_count']:.0f}")
        
        report.append("\n📈 SYSTEM PERFORMANCE (Validation):")
        perf = prediction['system_performance']
        if perf:
            report.append(f"    Recall:     {perf.get('recall', 'N/A'):.2%} (catches high-risk days)")
            report.append(f"    Precision:  {perf.get('precision', 'N/A'):.2%} (alert accuracy)")
            report.append(f"    F1 Score:   {perf.get('f1_score', 'N/A'):.3f}")
        else:
            report.append("    (Performance metrics not available)")
        
        report.append("\n" + "=" * 70)
        report.append("\n⚠️  This alert supplements, not replaces, safety judgment.")
        report.append("=" * 70)
        
        return "\n".join(report)


def main_example():
    """Example usage of the safety alert system."""
    
    print("🏗️  Safety Leading Indicators Dashboard")
    print("=" * 70)
    
    # Initialize system
    system = SafetyAlertSystem()
    
    # Example 1: Single day prediction
    print("\n📍 EXAMPLE 1: Single Day Prediction")
    print("-" * 70)
    
    prediction = system.predict_daily_risk(
        date="2023-02-04",
        vibration=28.5,
        temperature=32.0,
        humidity=65.0,
        worker_count=45,
        equipment_utilization=0.82
    )
    
    # Generate and print report
    report = system.generate_alert_report(prediction)
    print(report)
    
    # Example 2: Batch prediction from CSV
    print("\n\n📍 EXAMPLE 2: Batch Prediction from CSV")
    print("-" * 70)
    
    try:
        # Load data
        df = pd.read_csv("../data/construction_project_dataset.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Aggregate to daily
        df_daily = df.groupby(pd.Grouper(key='timestamp', freq='D')).agg({
            'temperature': 'mean',
            'humidity': 'mean',
            'vibration_level': 'mean',
            'worker_count': 'mean',
            'equipment_utilization_rate': 'mean'
        }).reset_index()
        
        # Remove empty days
        df_daily = df_daily[df_daily['worker_count'] > 0].reset_index(drop=True)
        
        # Predict
        predictions = system.batch_predict(df_daily.tail(7))  # Last 7 days
        
        print("\nLast 7 days risk assessment:")
        print("-" * 70)
        for _, pred in predictions.iterrows():
            risk_icon = "🔴" if pred['risk_level'] == 'HIGH RISK' else "🟢"
            print(f"{risk_icon} {pred['date']}: {pred['risk_level']}")
            if pred['triggered_factors']:
                for factor in pred['triggered_factors']:
                    print(f"     {factor}")
        
    except FileNotFoundError:
        print("⚠️  Data file not found. Skipping batch prediction example.")
    
    # Example 3: API-style JSON output
    print("\n\n📍 EXAMPLE 3: JSON API Response")
    print("-" * 70)
    
    json_output = json.dumps(prediction, indent=2)
    print(json_output)


if __name__ == "__main__":
    main_example()

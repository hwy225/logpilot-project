# Task 7: Weekly Operations Notes Generator

Auto-generates weekly operations notes combining insights from Time Overrun predictions and Safety alerts using Google Gemini LLM.

## 🎯 Purpose

Automatically draft weekly operations summaries that:
- Highlight high-risk projects (time overrun predictions)
- Summarize safety alerts and incidents
- Provide actionable recommendations
- Save PMs time (target: <2 min to review and finalize)

## 📦 Components

```
ops_notes/
├── generator.py          # Main script (WeeklyOpsNotesGenerator class)
├── prompt.txt            # LLM prompt template
├── test_generator.py     # Test/demo script
├── README.md             # This file
└── samples/              # Generated report outputs
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install google-generativeai python-dotenv
```

### 2. Set up API Key

**Option A: Use .env file (Recommended)**
```bash
# Create .env in project root
echo "GEMINI_API_KEY=your-key-here" > .env
```

**Option B: Environment variable**
```bash
export GEMINI_API_KEY='your-key-here'
```

Get API key from: https://makersuite.google.com/app/apikey

### 3. Run Test

```bash
python ops_notes/test_generator.py
```

Output saved to: `ops_notes/samples/week_2026_01_06.md`

## 💻 Usage

### Basic Usage

```python
from ops_notes.generator import WeeklyOpsNotesGenerator
import pandas as pd
import os

# Initialize
api_key = os.environ.get('GEMINI_API_KEY')
generator = WeeklyOpsNotesGenerator(gemini_api_key=api_key)

# Prepare project data (for time overrun)
projects = [
    {
        'project_id': 'Alpha_Tower',
        'features': {...}  # Project features for prediction
    },
    {
        'project_id': 'Beta_Bridge',
        'features': {...}
    }
]

# Prepare safety data (daily metrics)
safety_df = pd.DataFrame({
    'date': pd.date_range('2026-01-06', '2026-01-10'),
    'vibration_level': [22.5, 28.3, 24.1, 26.7, 23.9],
    'temperature': [28, 31, 29, 32, 30],
    'humidity': [65, 70, 68, 72, 69],
    'workers_onsite': [45, 52, 48, 55, 50],
    'equipment_count': [8, 10, 9, 11, 9]
})

# Generate report
report = generator.generate_weekly_report(
    projects_data=projects,
    safety_data=safety_df,
    week_start='2026-01-06',
    week_end='2026-01-10',
    output_path='ops_notes/samples/week_2026_01_06.md'
)

print(report)
```

## 📊 Report Structure

Generated reports include:

1. **Executive Summary** - 3-4 sentence overview
2. **Key Findings** - Schedule performance + Safety alerts
3. **Risk Analysis** - Prioritized issues with root causes
4. **Recommended Actions** - Specific, actionable interventions
5. **Outlook** - Trends to watch next week
6. **Raw Data Appendix** - Complete data reference

## 🔧 Customization

Edit `prompt.txt` to customize:
- Report structure and sections
- Tone and style
- Focus areas
- Output format

## 🔗 API Dependencies

1. **Time Overrun API** (`models/overrun_api.py`)
2. **Safety Alert System** (`safety/safety_dashboard.py`)
3. **Google Gemini API** (requires API key)

## 🐛 Troubleshooting

| Issue | Fix |
|-------|-----|
| `GEMINI_API_KEY not found` | Add to `.env` or `export GEMINI_API_KEY='your-key'` |
| Import errors | Run from project root |
| Model files not found | Check `models/saved_models/*.pkl` exist |
| LLM generation fails | Check API key and internet; fallback used |

---

**Status**: ✅ Production Ready  
**Target**: ≥70% PM acceptance, <2 min review time  
**Last Updated**: January 10, 2026

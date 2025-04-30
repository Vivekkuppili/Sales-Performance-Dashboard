# Sales Performance Dashboard & Lead Analysis

This project is an interactive sales analytics dashboard built with Python, Pandas, and Streamlit. It enables business users to forecast monthly revenue using machine learning (Holt-Winters), track KPIs (revenue, conversion rate, lead quality), segment leads, and identify top-performing salespeople and regions, all with interactive filters and rich visualizations.

## Features
- Data cleaning and validation
- KPI tracking (total revenue, profit, conversion rate, lead quality)
- Sales forecasting using Exponential Smoothing (ML)
- Segmentation by region, customer type, product, and salesperson
- Interactive filters and visualizations with Plotly
- Streamlit-based web dashboard

## How to Run
1. Place your sales dataset (e.g., `Sample - Superstore.csv`) in the project folder.
2. Install dependencies: `pip install -r requirements.txt`
3. Start the dashboard: `python -m streamlit run frontend.py`
4. Open the provided local URL in your browser.

## Files
- `backend.py`: Data processing, ML/AI logic, KPIs
- `frontend.py`: Streamlit UI and interactive dashboard
- `requirements.txt`: Python dependencies

## Requirements
- Python 3.8+
- See `requirements.txt` for packages

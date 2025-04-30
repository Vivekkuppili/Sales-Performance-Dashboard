import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.preprocessing import LabelEncoder

# File path
DATA_PATH = 'Sample - Superstore.csv'

def load_data():
    df = pd.read_csv(DATA_PATH, encoding='ISO-8859-1')
    return df

def clean_data(df):
    # Standardize column names
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
    # Parse dates
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'])
    # Drop duplicates
    df = df.drop_duplicates()
    # Handle missing values (simple fill or drop for demo)
    df = df.dropna(subset=['order_date', 'sales', 'customer_name', 'region', 'segment', 'category', 'sub-category', 'sales', 'profit', 'quantity'])
    # Convert sales and profit to numeric if needed
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    df['profit'] = pd.to_numeric(df['profit'], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df = df.dropna(subset=['sales', 'profit', 'quantity'])
    return df

def feature_engineering(df):
    # Monthly period
    df['month'] = df['order_date'].dt.to_period('M')
    # Lead quality: profit margin
    df['profit_margin'] = df['profit'] / df['sales']
    # Conversion rate (orders per customer per month)
    conversion = df.groupby(['month', 'customer_name']).size().groupby('month').mean()
    # Encode categorical for analysis
    for col in ['region', 'segment', 'category', 'sub-category', 'customer_name', 'sales_person']:
        if col in df.columns:
            df[col+'_enc'] = LabelEncoder().fit_transform(df[col])
    return df, conversion

def kpi_over_time(df):
    kpis = df.groupby('month').agg({
        'sales': 'sum',
        'profit': 'sum',
        'order_id': 'nunique',
        'customer_name': 'nunique',
        'profit_margin': 'mean',
        'quantity': 'sum'
    }).reset_index()
    kpis['conversion_rate'] = kpis['order_id'] / kpis['customer_name']
    return kpis

def segment_leads(df):
    # By customer type (segment), region, salesperson
    by_segment = df.groupby('segment').agg({'sales': 'sum', 'profit': 'sum', 'order_id': 'nunique'}).sort_values('sales', ascending=False)
    by_region = df.groupby('region').agg({'sales': 'sum', 'profit': 'sum', 'order_id': 'nunique'}).sort_values('sales', ascending=False)
    if 'sales_person' in df.columns:
        by_salesperson = df.groupby('sales_person').agg({'sales': 'sum', 'profit': 'sum', 'order_id': 'nunique'}).sort_values('sales', ascending=False)
    else:
        by_salesperson = None
    return by_segment, by_region, by_salesperson

def top_performers(df):
    # Top salespeople and regions
    top_regions = df.groupby('region')['sales'].sum().sort_values(ascending=False).head(5)
    if 'sales_person' in df.columns:
        top_salespeople = df.groupby('sales_person')['sales'].sum().sort_values(ascending=False).head(5)
    else:
        top_salespeople = None
    return top_regions, top_salespeople

def forecast_revenue(kpis, periods=3):
    # Forecast next N months using Holt-Winters
    model = ExponentialSmoothing(kpis['sales'], trend='add', seasonal='add', seasonal_periods=12)
    fit = model.fit()
    forecast = fit.forecast(periods)
    return forecast

# For Streamlit frontend
def get_dashboard_data():
    df = load_data()
    df = clean_data(df)
    df, conversion = feature_engineering(df)
    kpis = kpi_over_time(df)
    by_segment, by_region, by_salesperson = segment_leads(df)
    top_regions, top_salespeople = top_performers(df)
    forecast = forecast_revenue(kpis)
    return {
        'df': df,
        'kpis': kpis,
        'conversion': conversion,
        'by_segment': by_segment,
        'by_region': by_region,
        'by_salesperson': by_salesperson,
        'top_regions': top_regions,
        'top_salespeople': top_salespeople,
        'forecast': forecast
    }

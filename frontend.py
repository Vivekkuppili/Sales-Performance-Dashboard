import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from backend import get_dashboard_data

st.set_page_config(page_title='Sales Performance Dashboard', layout='wide')
st.title('Sales Performance Dashboard & Lead Analysis')

# Load data from backend
data = get_dashboard_data()
df = data['df']
kpis = data['kpis']
conversion = data['conversion']
by_segment = data['by_segment']
by_region = data['by_region']
by_salesperson = data['by_salesperson']
top_regions = data['top_regions']
top_salespeople = data['top_salespeople']
forecast = data['forecast']

# Sidebar filters
st.sidebar.header('Filters')
regions = df['region'].unique().tolist()
segments = df['segment'].unique().tolist()
products = df['category'].unique().tolist()
salespeople = df['sales_person'].unique().tolist() if 'sales_person' in df.columns else []

region_filter = st.sidebar.multiselect('Region', regions, default=regions)
segment_filter = st.sidebar.multiselect('Customer Segment', segments, default=segments)
product_filter = st.sidebar.multiselect('Product Category', products, default=products)
salesperson_filter = st.sidebar.multiselect('Salesperson', salespeople, default=salespeople) if salespeople else []

# Apply filters
df_filtered = df[
    df['region'].isin(region_filter) &
    df['segment'].isin(segment_filter) &
    df['category'].isin(product_filter)
]
if salespeople and salesperson_filter:
    df_filtered = df_filtered[df_filtered['sales_person'].isin(salesperson_filter)]

# KPIs
st.subheader('Key Performance Indicators')
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric('Total Revenue', f"${df_filtered['sales'].sum():,.0f}")
kpi2.metric('Total Profit', f"${df_filtered['profit'].sum():,.0f}")
kpi3.metric('Conversion Rate', f"{df_filtered['order_id'].nunique() / df_filtered['customer_name'].nunique():.2f}")
kpi4.metric('Avg. Profit Margin', f"{df_filtered['profit_margin'].mean():.2%}")

# Revenue trend
st.subheader('Monthly Revenue Trend')
# Convert Period columns to string for Plotly compatibility
monthly_sales = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M'))['sales'].sum().reset_index()
monthly_sales['order_date'] = monthly_sales['order_date'].astype(str)
fig1 = px.line(monthly_sales, x='order_date', y='sales', title='Monthly Revenue')
st.plotly_chart(fig1, use_container_width=True)

# Forecast chart
st.subheader('Revenue Forecast (Next 3 Months)')
# Convert Period columns to string for Plotly compatibility
kpis['month_str'] = kpis['month'].astype(str)
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=kpis['month_str'], y=kpis['sales'], mode='lines+markers', name='Historical'))
forecast_index = pd.period_range(kpis['month'].iloc[-1]+1, periods=len(forecast), freq='M').astype(str)
fig2.add_trace(go.Scatter(x=forecast_index, y=forecast, mode='lines+markers', name='Forecast'))
fig2.update_layout(title='Revenue Forecast', xaxis_title='Month', yaxis_title='Sales')
st.plotly_chart(fig2, use_container_width=True)

# Segment performance
st.subheader('Segment Performance')
st.dataframe(by_segment)

# Region performance
st.subheader('Region Performance')
st.dataframe(by_region)

# Top performers
st.subheader('Top Regions')
st.table(top_regions)
if top_salespeople is not None:
    st.subheader('Top Salespeople')
    st.table(top_salespeople)

# Lead quality
st.subheader('Lead Quality Over Time')
fig3 = px.line(kpis, x='month_str', y='profit_margin', title='Average Profit Margin Over Time')
st.plotly_chart(fig3, use_container_width=True)

# Conversion rate trend
st.subheader('Conversion Rate Trend')
fig4 = px.line(kpis, x='month_str', y='conversion_rate', title='Conversion Rate Over Time')
st.plotly_chart(fig4, use_container_width=True)

# Insights
st.subheader('Business Insights')
st.markdown(f"- **Highest Revenue Region:** {top_regions.index[0]} (${top_regions.iloc[0]:,.0f})")
if top_salespeople is not None:
    st.markdown(f"- **Top Salesperson:** {top_salespeople.index[0]} (${top_salespeople.iloc[0]:,.0f})")
st.markdown(f"- **Best Performing Segment:** {by_segment.index[0]} (${by_segment.iloc[0]['sales']:,.0f})")
st.markdown(f"- **Average Conversion Rate:** {kpis['conversion_rate'].mean():.2f}")

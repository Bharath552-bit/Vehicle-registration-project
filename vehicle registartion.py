import streamlit as st
import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
import plotly.express as px

# --- 1. Data Generation (Mock Data) ---
# This function generates a sample DataFrame. In a real-world scenario, you would
# replace this with your data loading function (e.g., from a CSV, database, or API).
# Instructions to replace this data are provided below.

def generate_mock_data():
    """Generates a sample DataFrame for vehicle registration data."""
    np.random.seed(42)
    
    # We now define start_date as a Timestamp for consistency
    start_date = pd.Timestamp.now() - relativedelta(years=3)
    # Corrected frequency from 'M' to 'ME' to avoid FutureWarning
    dates = pd.date_range(start_date, periods=3 * 12, freq='ME')
    
    manufacturers = ['Toyota', 'Honda', 'Maruti', 'Ford', 'Tesla']
    categories = ['2W', '4W', 'Commercial']
    
    data = []
    for date in dates:
        for manufacturer in manufacturers:
            for category in categories:
                # Generate random vehicle counts for each month
                base_vehicles = np.random.randint(5000, 20000)
                # Introduce a slight positive trend over time
                # Ensure consistent types by subtracting a Timestamp from a Timestamp
                trend_factor = (date - start_date).days / 1000
                vehicles = int(base_vehicles * (1 + 0.05 * trend_factor) + np.random.normal(0, 1000))
                
                data.append([date, category, manufacturer, vehicles])
    
    df = pd.DataFrame(data, columns=['registration_date', 'vehicle_category', 'manufacturer', 'total_vehicles'])
    return df

# --- 2. Data Loading & Preprocessing ---
# To use your own data, replace the line below with a data loading method.
# For example, to load from a CSV file:
# df = pd.read_csv('your_data.csv')
# Make sure your CSV has columns named 'registration_date', 'vehicle_category',
# 'manufacturer', and 'total_vehicles'.
#
# If your date column is not in datetime format, convert it like this:
# df['registration_date'] = pd.to_datetime(df['registration_date'])
#
# If you are able to scrape the data from the provided website, a tool like
# Selenium would be required to interact with the dashboard.
# Once you have the data, ensure it is in the same format as the mock data.

df = generate_mock_data()
df['year'] = df['registration_date'].dt.year
df['quarter'] = df['registration_date'].dt.quarter

# --- 3. Dashboard UI Layout ---
st.set_page_config(layout="wide", page_title="Vehicle Registration Dashboard", page_icon="🚗")

st.title("Vehicle Registration Dashboard")
st.markdown("Investor's perspective: YoY and QoQ Growth Analysis")

# --- Sidebar for Filters ---
st.sidebar.header("Filters")

# Date Range Slider
min_date = df['registration_date'].min().date()
max_date = df['registration_date'].max().date()
date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)
df_filtered = df[(df['registration_date'].dt.date >= date_range[0]) & (df['registration_date'].dt.date <= date_range[1])]

# Multi-select for Vehicle Category
selected_categories = st.sidebar.multiselect(
    "Select Vehicle Category",
    options=df_filtered['vehicle_category'].unique(),
    default=df_filtered['vehicle_category'].unique()
)
df_filtered = df_filtered[df_filtered['vehicle_category'].isin(selected_categories)]

# Multi-select for Manufacturer
selected_manufacturers = st.sidebar.multiselect(
    "Select Manufacturer",
    options=df_filtered['manufacturer'].unique(),
    default=df_filtered['manufacturer'].unique()
)
df_filtered = df_filtered[df_filtered['manufacturer'].isin(selected_manufacturers)]

# Check if filtered data is empty
if df_filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# --- 4. Key Metrics and Calculations ---
def calculate_growth(df_input, period='YoY'):
    """Calculates Year-over-Year or Quarter-over-Quarter growth."""
    if df_input.empty:
        return 0, 0
    
    df_agg = df_input.groupby(df_input['registration_date'].dt.to_period('M'))['total_vehicles'].sum().reset_index()
    df_agg['registration_date'] = df_agg['registration_date'].dt.to_timestamp()

    current_period_end = df_agg['registration_date'].max()
    current_value = df_agg[df_agg['registration_date'] == current_period_end]['total_vehicles'].values[0]

    if period == 'YoY':
        previous_period_end = current_period_end - relativedelta(years=1)
        if previous_period_end in df_agg['registration_date'].values:
            previous_value = df_agg[df_agg['registration_date'] == previous_period_end]['total_vehicles'].values[0]
            if previous_value != 0:
                growth_rate = ((current_value - previous_value) / previous_value) * 100
            else:
                growth_rate = 0
        else:
            growth_rate = 0
            previous_value = 0
        return growth_rate, previous_value
    
    elif period == 'QoQ':
        current_quarter = pd.to_datetime(current_period_end).to_period('Q')
        previous_quarter = current_quarter - 1
        
        # Aggregate by quarter
        df_quarterly = df_input.groupby(df_input['registration_date'].dt.to_period('Q'))['total_vehicles'].sum().reset_index()
        df_quarterly['registration_date'] = df_quarterly['registration_date'].astype(str)
        
        current_quarter_value = df_quarterly[df_quarterly['registration_date'] == str(current_quarter)]['total_vehicles'].values
        previous_quarter_value = df_quarterly[df_quarterly['registration_date'] == str(previous_quarter)]['total_vehicles'].values
        
        if len(current_quarter_value) > 0 and len(previous_quarter_value) > 0:
            current_value = current_quarter_value[0]
            previous_value = previous_quarter_value[0]
            if previous_value != 0:
                growth_rate = ((current_value - previous_value) / previous_value) * 100
            else:
                growth_rate = 0
        else:
            growth_rate = 0
            current_value = 0
            previous_value = 0
        
        return growth_rate, previous_value

yoy_growth, _ = calculate_growth(df_filtered, period='YoY')
qoq_growth, _ = calculate_growth(df_filtered, period='QoQ')

col1, col2 = st.columns(2)
with col1:
    st.metric(label="YoY Growth", value=f"{yoy_growth:.2f}%", delta=f"{yoy_growth:.2f}%")
with col2:
    st.metric(label="QoQ Growth", value=f"{qoq_growth:.2f}%", delta=f"{qoq_growth:.2f}%")

# --- 5. Visualizations for Trends and % Change ---

st.header("Trends by Vehicle Category")
category_trend_df = df_filtered.groupby(['registration_date', 'vehicle_category'])['total_vehicles'].sum().reset_index()
fig_category_trend = px.line(
    category_trend_df,
    x='registration_date',
    y='total_vehicles',
    color='vehicle_category',
    title='Monthly Vehicle Registration by Category'
)
st.plotly_chart(fig_category_trend, use_container_width=True)

st.header("Trends by Manufacturer")
manufacturer_trend_df = df_filtered.groupby(['registration_date', 'manufacturer'])['total_vehicles'].sum().reset_index()
fig_manufacturer_trend = px.line(
    manufacturer_trend_df,
    x='registration_date',
    y='total_vehicles',
    color='manufacturer',
    title='Monthly Vehicle Registration by Manufacturer'
)
st.plotly_chart(fig_manufacturer_trend, use_container_width=True)

st.header("Breakdown of Total Vehicles by Category")
category_breakdown_df = df_filtered.groupby('vehicle_category')['total_vehicles'].sum().reset_index()
fig_category_pie = px.pie(
    category_breakdown_df,
    values='total_vehicles',
    names='vehicle_category',
    title='Total Vehicles by Category'
)
st.plotly_chart(fig_category_pie, use_container_width=True)

st.header("Breakdown of Total Vehicles by Manufacturer")
manufacturer_breakdown_df = df_filtered.groupby('manufacturer')['total_vehicles'].sum().reset_index()
fig_manufacturer_pie = px.pie(
    manufacturer_breakdown_df,
    values='total_vehicles',
    names='manufacturer',
    title='Total Vehicles by Manufacturer'
)
st.plotly_chart(fig_manufacturer_pie, use_container_width=True)

import streamlit as st
import pandas as pd

def prepare_data():
    # Load the datasets
    business_df = pd.read_csv("Marketing Intelligence Dashboard/business.csv")
    facebook_df = pd.read_csv("Marketing Intelligence Dashboard/Facebook.csv")
    google_df = pd.read_csv("Marketing Intelligence Dashboard/Google.csv")
    tiktok_df = pd.read_csv("Marketing Intelligence Dashboard/TikTok.csv")

    # Add a 'source' column to each marketing DataFrame
    facebook_df['source'] = 'Facebook'
    google_df['source'] = 'Google'
    tiktok_df['source'] = 'TikTok'

    # Combine the marketing data
    marketing_df = pd.concat([facebook_df, google_df, tiktok_df])

    # Convert date columns to datetime objects
    marketing_df['date'] = pd.to_datetime(marketing_df['date'])
    business_df['date'] = pd.to_datetime(business_df['date'])

    # Merge the marketing and business data
    df = pd.merge(marketing_df, business_df, on='date', how='left')

    # Create new metrics
    df['cpc'] = df['spend'] / df['clicks']
    df['ctr'] = df['clicks'] / df['impression'] * 100
    df['roas'] = df['attributed revenue'] / df['spend']
    
    # Rename columns for clarity
    df.rename(columns={'# of orders': 'orders', '# of new orders': 'new_orders', 'new customers': 'new_customers', 'total revenue': 'total_revenue', 'gross profit': 'gross_profit'}, inplace=True)

    return df

st.set_page_config(layout="wide")

df = prepare_data()

st.title("Marketing Intelligence Dashboard")

st.sidebar.title("Filters")

# Date range filter
min_date = df['date'].min()
max_date = df['date'].max()
start_date, end_date = st.sidebar.date_input("Date range", [min_date, max_date])

# Source filter
sources = st.sidebar.multiselect("Source", df['source'].unique(), df['source'].unique())

# Filter the data
filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date)) & (df['source'].isin(sources))]

# KPIs
total_spend = filtered_df['spend'].sum()
total_revenue = filtered_df['total_revenue'].sum()
roas = total_revenue / total_spend
new_customers = filtered_df['new_customers'].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Spend", f"${total_spend:,.0f}")
col2.metric("Total Revenue", f"${total_revenue:,.0f}")
col3.metric("ROAS", f"{roas:,.2f}")
col4.metric("New Customers", f"{new_customers:,.0f}")

# Charts
st.header("Spend and Revenue Over Time")
st.line_chart(filtered_df.groupby('date')[['spend', 'total_revenue']].sum())

st.header("Performance by Channel")
st.bar_chart(filtered_df.groupby('source')[['spend', 'total_revenue']].sum())

st.header("Performance by State")
st.bar_chart(filtered_df.groupby('state')[['spend', 'total_revenue']].sum())

st.header("Spend vs. Revenue")
st.scatter_chart(data=filtered_df, x='spend', y='total_revenue', color='source')

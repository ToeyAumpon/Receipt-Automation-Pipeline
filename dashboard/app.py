import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import json
import os

# --- Connect to Google Sheets ---
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def get_data():
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    if creds_json:
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    else:
        creds = Credentials.from_service_account_file(
            'google_credentials.json', scopes=SCOPES
        )

    client = gspread.authorize(creds)
    sheet = client.open("Receipt Tracker").sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# --- Page Setup ---
st.set_page_config(
    page_title="Receipt Tracker",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Receipt Tracker Dashboard")
st.markdown("---")

# --- Load Data ---
try:
    df = get_data()
except Exception as e:
    st.error(f"Could not load data: {e}")
    st.stop()

if df.empty:
    st.warning("No data found in Google Sheets.")
    st.stop()

# --- Clean Data ---
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Amount', 'Date'])
df['Month'] = df['Date'].dt.strftime('%Y/%m')

# --- Filters FIRST ---
st.subheader("🔍 Filter")
col_f1, col_f2 = st.columns(2)

with col_f1:
    stores = ['All'] + sorted(df['Store'].unique().tolist())
    selected_store = st.selectbox("Filter by Store", stores)

with col_f2:
    months = ['All'] + sorted(df['Month'].unique().tolist(), reverse=True)
    selected_month = st.selectbox("Filter by Month", months)

# --- Apply Filters ---
filtered_df = df.copy()
if selected_store != 'All':
    filtered_df = filtered_df[filtered_df['Store'] == selected_store]
if selected_month != 'All':
    filtered_df = filtered_df[filtered_df['Month'] == selected_month]

st.markdown("---")

# --- Summary Cards (based on filtered data) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Total Spent", f"¥{filtered_df['Amount'].sum():,.0f}")

with col2:
    st.metric("🧾 Total Transactions", len(filtered_df))

with col3:
    st.metric("📅 Last Updated", df['Date'].max().strftime('%Y/%m/%d'))

st.markdown("---")

# --- Charts ---
col4, col5 = st.columns(2)

with col4:
    st.subheader("📊 Spending by Store")
    store_data = filtered_df.groupby('Store')['Amount'].sum().sort_values(ascending=False)
    st.bar_chart(store_data)

with col5:
    st.subheader("📈 Spending Over Time")
    time_data = filtered_df.groupby('Date')['Amount'].sum()
    st.line_chart(time_data)

st.markdown("---")

# --- Transactions Table ---
st.subheader("📋 Transactions")
st.dataframe(
    filtered_df[['Date', 'Time', 'Store', 'Amount', 'Currency', 'Approval No']]
    .sort_values('Date', ascending=False)
    .reset_index(drop=True),
    use_container_width=True
)
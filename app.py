import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('2025 311 Requests Dashboard')
st.write('Explore 311 service requests by selecting a date range.')

DATA_FILE = '311_2025_dashboard.csv'
df = pd.read_csv(DATA_FILE)
df['request_date'] = pd.to_datetime(df['request_date'], errors='coerce')

valid_dates = df['request_date'].dropna()
if valid_dates.empty:
    st.error('No valid request dates were found in the dataset.')
    st.stop()

min_date = valid_dates.min().date()
max_date = valid_dates.max().date()

start_date = st.date_input('Start Date', value=min_date, min_value=min_date, max_value=max_date)
end_date = st.date_input('End Date', value=max_date, min_value=min_date, max_value=max_date)

if start_date > end_date:
    st.error('Start Date must be on or before End Date.')
    st.stop()

filtered_df = df[
    (df['request_date'].dt.date >= start_date) &
    (df['request_date'].dt.date <= end_date)
].copy()

st.write(f'Requests in selected period: {len(filtered_df):,}')

if filtered_df.empty:
    st.warning('No requests found for the selected dates.')
    st.stop()

st.subheader('Top 10 Types of 311 Requests')
top_requests = filtered_df['service_name'].value_counts().head(10).sort_values()
fig1, ax1 = plt.subplots(figsize=(8, 5))
top_requests.plot(kind='barh', ax=ax1)
ax1.set_xlabel('Number of Requests')
ax1.set_ylabel('Service Type')
fig1.tight_layout()
st.pyplot(fig1)
plt.close(fig1)

st.subheader('311 Requests Over Time')
requests_by_day = filtered_df.groupby(filtered_df['request_date'].dt.date).size()
fig2, ax2 = plt.subplots(figsize=(9, 4))
requests_by_day.plot(kind='line', ax=ax2)
ax2.set_xlabel('Request Date')
ax2.set_ylabel('Number of Requests')
fig2.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

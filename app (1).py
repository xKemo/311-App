import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title("2025 311 Requests Dashboard")
st.write("Explore 311 requests by date, responsible agency, and day of the week.")

DATA_FILE = "311_2025_dashboard.csv"
df = pd.read_csv(DATA_FILE)
df["request_date"] = pd.to_datetime(df["request_date"], errors="coerce")
df = df.dropna(subset=["request_date"])

start_date = st.date_input("Start Date", value=pd.to_datetime("2025-10-01").date(), min_value=pd.to_datetime("2025-01-01").date(), max_value=pd.to_datetime("2025-12-31").date())
end_date = st.date_input("End Date", value=pd.to_datetime("2025-12-31").date(), min_value=pd.to_datetime("2025-01-01").date(), max_value=pd.to_datetime("2025-12-31").date())

if start_date > end_date:
    st.error("Start Date must be on or before End Date.")
    st.stop()

filtered_df = df[
    (df["request_date"].dt.date >= start_date)
    & (df["request_date"].dt.date <= end_date)
].copy()

st.metric("Requests in Selected Period", f"{len(filtered_df):,}")

if filtered_df.empty:
    st.warning("No requests found for these dates.")
    st.stop()

st.subheader("Top 10 Responsible Agencies for 311 Requests")
agency_counts = (
    filtered_df["agency_responsible"]
    .value_counts()
    .head(10)
    .sort_values()
)
fig1, ax1 = plt.subplots(figsize=(10, 6))
agency_counts.plot(kind="barh", ax=ax1, color="skyblue")
ax1.set_xlabel("Number of Requests")
ax1.set_ylabel("Agency")
fig1.tight_layout()
st.pyplot(fig1)
plt.close(fig1)

st.subheader("311 Requests by Day of the Week")
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_counts = (
    filtered_df["day_of_week"]
    .value_counts()
    .reindex(day_order, fill_value=0)
)
fig2, ax2 = plt.subplots(figsize=(9, 5))
day_counts.plot(kind="bar", ax=ax2, color="coral")
ax2.set_xlabel("Day of the Week")
ax2.set_ylabel("Number of Requests")
ax2.tick_params(axis="x", rotation=45)
fig2.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

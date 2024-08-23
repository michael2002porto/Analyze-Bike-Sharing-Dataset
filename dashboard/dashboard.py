import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

sns.set(style='dark')

# Load data
day_df = pd.read_excel("day_cleaned.xlsx")
hour_df = pd.read_excel("hour_cleaned.xlsx")

# Convert datetime columns
day_df['datetime'] = pd.to_datetime(day_df['datetime'])
hour_df['datetime'] = pd.to_datetime(hour_df['datetime'])

# Sidebar for date selection
with st.sidebar:
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=day_df["datetime"].min(),
        max_value=day_df["datetime"].max(),
        value=[day_df["datetime"].min(), day_df["datetime"].max()]
    )

main_df_days = day_df[(day_df["datetime"] >= str(start_date)) & (day_df["datetime"] <= str(end_date))]
main_df_hour = hour_df[(hour_df["datetime"] >= str(start_date)) & (hour_df["datetime"] <= str(end_date))]

# Visualization Section

st.header(':bike: Bike Sharing Analysis - Michael Natanael')

# 1. Hourly and Daily Distribution
st.subheader('Hourly and Daily Distribution of Bike Rentals')

# Hourly distribution by season
fig, ax = plt.subplots()
sns.pointplot(data=main_df_hour[['hour', 'total_count', 'season']], x='hour', y='total_count', hue='season', ax=ax)
ax.set(title="Season-wise Hourly Distribution of Counts")
st.pyplot(fig)

# Hourly distribution by weekday
fig, ax = plt.subplots(figsize=(10, 5))
sns.pointplot(data=main_df_hour[['hour', 'total_count', 'weekday']], x='hour', y='total_count', hue='weekday', ax=ax)
ax.set(title="Weekday-wise Hourly Distribution of Counts")
st.pyplot(fig)

# Daily distribution by season
fig, ax = plt.subplots()
sns.lineplot(data=main_df_days[['weekday', 'total_count', 'season']], x='weekday', y='total_count', hue='season', ax=ax)
ax.set(title="Season-wise Daily Distribution of Counts")
st.pyplot(fig)

# Monthly distribution
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=main_df_days[['month', 'total_count']], x="month", y="total_count", ax=ax)
ax.set(title="Monthly Distribution of Counts")
st.pyplot(fig)

# 2. Correlation Analysis
st.subheader('Correlation Analysis')

corrMatt = main_df_days[["temp", "atemp", "humidity", "windspeed", "casual", "registered", "total_count"]].corr()
mask = np.array(corrMatt)
mask[np.tril_indices_from(mask)] = False

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corrMatt, mask=mask, vmax=.8, square=True, annot=True, ax=ax)
ax.set(title="Correlation Matrix (Day Data)")
st.pyplot(fig)

# 3. Clustering Analysis
st.subheader('Clustering Analysis')

# Clustering based on is_holiday and is_workingday
fig, ax = plt.subplots(1, 2, figsize=(20, 8))

# Day Data
sns.countplot(x='is_holiday', data=main_df_days, ax=ax[0])
ax[0].set(title='Bike Rentals on Holidays vs. Non-Holidays')

sns.countplot(x='is_workingday', data=main_df_days, ax=ax[1])
ax[1].set(title='Bike Rentals on Working Days vs. Non-Working Days')

st.pyplot(fig)

# 4. RFM Analysis
st.subheader('RFM Analysis')

current_date = main_df_days['datetime'].max()

# RFM for Registered Customers
rfm_df_registered = main_df_days.groupby('registered').agg({
    'datetime': lambda x: (current_date - x.max()).days,
    'rec_id': 'count',
    'total_count': 'sum'
}).reset_index()
rfm_df_registered.columns = ['registered', 'Recency', 'Frequency', 'Monetary']
st.write("Registered Customer RFM:")
st.write(rfm_df_registered.head())

# RFM for Casual Customers
rfm_df_casual = main_df_days.groupby('casual').agg({
    'datetime': lambda x: (current_date - x.max()).days,
    'rec_id': 'count',
    'total_count': 'sum'
}).reset_index()
rfm_df_casual.columns = ['casual', 'Recency', 'Frequency', 'Monetary']
st.write("Casual Customer RFM:")
st.write(rfm_df_casual.head())

# Conclusion
st.subheader('Conclusions')
st.write("""
1. The highest bike rentals occurred in the Fall season, particularly in June and September, on Thursdays, Fridays, and Saturdays, and between 17:00 - 18:00 hours.
2. Registered customers show a strong correlation (0.9) with the total bike rentals, while casual customers have a moderate correlation (0.6).
""")

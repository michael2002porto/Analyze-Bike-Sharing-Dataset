import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def get_total_count_by_hour_df(hour_df):
  hour_count_df =  hour_df.groupby(by="hour").agg({"total_count": ["sum"]})
  return hour_count_df

def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query(str('datetime >= "2011-01-01" and datetime < "2012-12-31"'))
    return day_df_count_2011

def total_registered_df(day_df):
   reg_df =  day_df.groupby(by="datetime").agg({
      "registered": "sum"
    })
   reg_df = reg_df.reset_index()
   reg_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg_df

def total_casual_df(day_df):
   cas_df =  day_df.groupby(by="datetime").agg({
      "casual": ["sum"]
    })
   cas_df = cas_df.reset_index()
   cas_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas_df

def sum_order (hour_df):
    sum_order_items_df = hour_df.groupby("hour").total_count.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def macem_season (day_df): 
    season_df = day_df.groupby(by="season").total_count.sum().reset_index() 
    return season_df

day_df = pd.read_excel("day_cleaned.xlsx")
hour_df = pd.read_excel("hour_cleaned.xlsx")

datetime_columns = ["datetime"]
day_df.sort_values(by="datetime", inplace=True)
day_df.reset_index(inplace=True)   

hour_df.sort_values(by="datetime", inplace=True)
hour_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])

min_date_days = day_df["datetime"].min()
max_date_days = day_df["datetime"].max()

min_date_hour = hour_df["datetime"].min()
max_date_hour = hour_df["datetime"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_days = day_df[(day_df["datetime"] >= str(start_date)) & 
                       (day_df["datetime"] <= str(end_date))]

main_df_hour = hour_df[(hour_df["datetime"] >= str(start_date)) & 
                        (hour_df["datetime"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = macem_season(main_df_hour)

#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Sharing :sparkles:')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_df_count_2011.total_count.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

st.subheader("Performa penjualan perusahaan dalam beberapa tahun terakhir")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    day_df["datetime"],
    day_df["total_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("pada jam berapa yang paling banyak dan paling sedikit disewa?")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(x="hour", y="total_count", data=sum_order_items_df.head(5), palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("hour (PM)", fontsize=30)
ax[0].set_title("Jam dengan banyak penyewa sepeda", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="hour", y="total_count", data=sum_order_items_df.sort_values(by="hour", ascending=True).head(5), palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#90CAF9"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("hour (AM)",  fontsize=30)
ax[1].set_title("Jam dengan sedikit penyewa sepeda", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)
st.subheader("musim apa yang paling banyak disewa?")

colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9"]
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
        y="total_count", 
        x="season",
        data=season_df.sort_values(by="season", ascending=False),
        palette=colors,
        ax=ax
    )
ax.set_title("Grafik Antar Musim", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.subheader("Perbandingan Customer yang Registered dengan casual")

labels = 'casual', 'registered'
sizes = [18.8, 81.2]
explode = (0, 0.1) 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',colors=["#D3D3D3", "#90CAF9"],
        shadow=True, startangle=90)
ax1.axis('equal')  

st.pyplot(fig1)

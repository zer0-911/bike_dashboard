import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_daily_bike_df(df):
    daily_bike_df = df.resample(rule='d', on='Date').agg({
        "instant": "nunique",
        "count": "sum"
    })
    daily_bike_df = daily_bike_df.reset_index()

    return daily_bike_df

# Load cleaned data
all_df = pd.read_csv("dashboard/main_data.csv")

datetime_columns = ["Date"]
all_df.sort_values(by="Date", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["Date"].min()
max_date = all_df["Date"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("./dashboard/img/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["Date"] >= str(start_date)) & 
                (all_df["Date"] <= str(end_date))]

daily_bike_df = create_daily_bike_df(main_df)

# plot number of daily orders (2021)
st.header('Bike Sharing Dashboard :rocket:')
st.subheader('Daily Bike')

total_bike = daily_bike_df["count"].sum()
st.metric("Total Bike", value=total_bike)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_bike_df["Date"],
    daily_bike_df["count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader("Holiday & Weekday Data")
tab1, tab2 = st.tabs(["Holiday", "Weekday"])
 
with tab1:
    st.subheader("Holiday Data")
    fig, ax = plt.subplots(figsize=(16, 8))
    
    sns.barplot(x='holiday',y='count',data=main_df,palette="rocket",)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    st.pyplot(fig)
 
with tab2:
    st.subheader("Weekday Data")
    fig, ax = plt.subplots(figsize=(16, 8))
    main_df['weekday']=main_df.weekday.map({0:'Sun',1:'Mon',2:'Tue',3:'Wed',4:'Thu',5:'Fri',6:'Sat'})
    sns.barplot(x='weekday',y='count',data=main_df,palette="rocket",)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    st.pyplot(fig)

st.subheader("Season Data")
fig, ax = plt.subplots(figsize=(16, 8))
main_df['season']=main_df.season.map({1: 'spring', 2: 'summer',3:'fall', 4:'winter'})
sns.barplot(x='season',y='count',data=main_df,palette="muted",)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)
with st.expander("See explanation"):
    st.write(
        """Based on the visualization above, it is known that **autumn** is the **highest** compared to other seasons. Smallest use of bicycles in **spring** season.
        """
    )
st.caption('Copyright © Iqbal 2023')
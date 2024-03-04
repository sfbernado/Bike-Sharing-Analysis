import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
sns.set(style='dark')

# Load the cleaned dataset

df = pd.read_csv('https://raw.githubusercontent.com/sfbernado/Bike-Sharing-Analysis/main/data/cleaned_day.csv')
df['date'] = pd.to_datetime(df['date'])

# Create function

def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='date').agg({
        "total_users": "sum",
        "casual_users": "sum",
        "registered_users": "sum"
    }).reset_index()
    
    return daily_rentals_df

def count_users_by_day_of_week(df):
    daily_user_type_df = df.groupby('day').agg({
        'casual_users': 'sum',
        'registered_users': 'sum'
    }).reset_index()

    return daily_user_type_df

# filter components

min_date = df['date'].min()
max_date = df['date'].max()

st.set_page_config(
    page_title="Bike Sharing Analysis",
    page_icon="📊",
    layout="wide"
)

# Sidebar

with st.sidebar:
    st.image('https://i.pinimg.com/474x/5d/b1/37/5db137e0973b20a77384eff400c7e113.jpg')

    start_date, end_date = st.date_input(
        label='Select Date Range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df['date'] >= str(start_date)) & 
             (df['date'] <= str(end_date))]

daily_rentals_df = create_daily_rentals_df(main_df)
daily_user_type_df = count_users_by_day_of_week(main_df)

# Title

st.title(':bar_chart: Bike Sharing Analysis Dashboard')

st.subheader('Overall Rental Statistics')

col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = main_df['total_users'].sum()
    st.metric('Total Rentals Bike', value=f'{total_rentals:,}')

with col2:
    total_casual = main_df['casual_users'].sum()
    st.metric('Total Casual Users', value=f'{total_casual:,}')

with col3:
    total_registered = main_df['registered_users'].sum()
    st.metric('Total Registered Users', value=f'{total_registered:,}')

st.markdown("---")

# Daily Rentals

st.subheader('Daily Count of Rentals Bike')

fig = px.line(
    daily_rentals_df,
    x='date',
    y=['total_users', 'casual_users', 'registered_users'],
    color_discrete_sequence=['red', 'blue', 'green'],
    markers=True,
)
st.plotly_chart(fig)

# Count of casual and registered users by day of the week

st.subheader('Count of Casual Users and Registered Users by Day of The Week')

fig2 = px.bar(
    daily_user_type_df,
    x='day',
    y=['casual_users', 'registered_users'],
    color_discrete_sequence=['red', 'blue'],
    barmode='group',
)
st.plotly_chart(fig2)

# Comparison of casual and registered users by day of the week

st.subheader('Comparison of Casual Users and Registered Users by Day of The Week')

fig3 = px.pie(
    daily_user_type_df,
    values=[daily_user_type_df['casual_users'].sum(), daily_user_type_df['registered_users'].sum()],
    names=['Casual Users', 'Registered Users'],
    color_discrete_sequence=['blue', 'red'],
)
st.plotly_chart(fig3)

# Footer

st.markdown("---")

st.caption('© 2024 Bike Sharing Analysis | Made with ❤️ by [Stanislaus Frans Bernado](https://www.linkedin.com/in/stanislausfb/)')
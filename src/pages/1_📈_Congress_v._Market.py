import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Congress v. Market", page_icon="📈")

st.markdown("# Congress versus the Market")
st.sidebar.header("Plotting")
st.write(
    """
    This page compares the cumulative returns of the S&P 500 index to the cumulative 
    returns of all Congress members.
    """
)

# LOAD S&P500 DATA ONCE
@st.cache_resource
def load_sp500_data():
    # https://github.com/adrianmross/congress_trades_dashboard/blob/main/data/outputs/s%26p500_returns.csv.gz
    path = "s%26p500_returns.csv.gz"
    if not os.path.exists(path):
        path = f"https://github.com/adrianmross/congress_trades_dashboard/raw/main/data/outputs/{path}"

    data = pd.read_csv(
        path,
        parse_dates=["date"],
        index_col="date",
    )

    return data

# LOAD CONGRESS RETURNS DATA ONCE
@st.cache_resource
def load_congress_data():
    # https://github.com/adrianmross/congress_trades_dashboard/blob/main/data/outputs/congress_returns.csv.gz
    path = "congress_returns.csv.gz"
    if not os.path.exists(path):
        path = f"https://github.com/adrianmross/congress_trades_dashboard/raw/main/data/outputs/{path}"

    data = pd.read_csv(
        path,
        parse_dates=["date"],
        index_col=["name", "date"],
    )

    return data

sp500_data = load_sp500_data()
congress_data = load_congress_data()

st.write(congress_data.head())

# # Calculating average cumulative returns for S&P 500
# sp500_cum_returns = sp500_data.groupby['cum_return'].reset_index()

# # Calculating average cumulative returns for all Congress members
# congress_avg_cum_returns = congress_data.groupby('date')['cum_return'].mean().reset_index()

# # Merging both dataframes on date for comparison
# merged_data = pd.merge(sp500_cum_returns, congress_avg_cum_returns, on='date', suffixes=('_sp500', '_congress'))

# st.write(merged_data)

# # Plotting
# fig = px.line(merged_data, x='date', y=['cum_return_sp500', 'cum_return_congress'],
#               labels={'value': 'Average Cumulative Return', 'variable': 'Series'},
#               title='Average Cumulative Returns: S&P 500 vs Congress')

# st.plotly_chart(fig, use_container_width=True)
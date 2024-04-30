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

# redo cum returns for both datasets to calc cum returns from 2020-01-01
sp500_cut = sp500_data.loc["2020-01-01":].copy()
sp500_cut["cum_return"] = (1 + sp500_cut["daily_return"]).cumprod() - 1

congress_cut = congress_data.loc["2020-01-01":].copy()
congress_cut["cum_return"] = (1 + congress_cut["return"]).groupby("name").cumprod() - 1

# plot congress_cut cum returns distribution by congress member
# remove donald s. beyer, jr. as outlier
congress_cut = congress_cut.drop("Donald S. Beyer, Jr.", level="name")
# fig = px.line(congress_cut.reset_index(), x="date", y="cum_return", color="name", title="Congress Members Cumulative Returns")

# st.plotly_chart(fig, use_container_width=True)


# # Calculating average cumulative returns for all Congress members
congress_avg_cum_returns = congress_cut.groupby('date')['cum_return'].mean().reset_index()

# get top 50 congress member average cumulative returns
top_50_congress = congress_cut.groupby('name')['cum_return'].last().sort_values(ascending=False).head(50)
# st.write(top_50_congress)
top_50_congress_avg_cum_returns = congress_cut[congress_cut.index.get_level_values('name').isin(top_50_congress.index)].groupby('date')['cum_return'].mean().reset_index()
# cut off anything before 2020-01-01
top_50_congress_avg_cum_returns = top_50_congress_avg_cum_returns.loc[top_50_congress_avg_cum_returns['date'] >= '2020-01-01']

# Merging both dataframes on date for comparison
merged_data = pd.merge(sp500_cut, congress_avg_cum_returns, on='date', suffixes=('_sp500', '_congress'))
# merged_data = pd.merge(merged_data, top_50_congress_avg_cum_returns, on='date', suffixes=('', '_top_50'))

# Plotting
fig = px.line(merged_data, x='date', y=['cum_return_sp500', 'cum_return_congress'],
              labels={'value': 'Average Cumulative Return', 'variable': 'Series'},
              title='Cumulative Returns: S&P 500 vs Congress')

# relable the legend cum_return_sp500 to S&P 500 and cum_return_congress to Congress Average
fig.for_each_trace(lambda t: t.update(name='S&P 500' if t.name == 'cum_return_sp500' else 'Congress Average'))

# plot top 50 congress members average cumulative returns on top
fig.add_scatter(x=top_50_congress_avg_cum_returns['date'], y=top_50_congress_avg_cum_returns['cum_return'], mode='lines', name='Top 50 Congress Average')

# fig = px.line(merged_data, x='date', y=['cum_return', 'cum_return_top_50'],
#                 labels={'value': 'Average Cumulative Return', 'variable': 'Series'},
#                 title='Average Cumulative Returns: S&P 500 vs Congress')

st.plotly_chart(fig, use_container_width=True)
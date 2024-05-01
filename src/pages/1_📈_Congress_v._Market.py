import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Congress v. Market", 
    page_icon="📈",
    layout="wide",)

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

# LOAD INSIDER RETURNS DATA ONCE
@st.cache_resource
def load_insider_data():
    # https://github.com/adrianmross/congress_trades_dashboard/blob/main/data/outputs/insider_returns.csv
    path = "insider_returns.csv"
    if not os.path.exists(path):
        path = f"https://github.com/adrianmross/congress_trades_dashboard/raw/main/data/outputs/{path}"

    data = pd.read_csv(
        path,
        parse_dates=["date"],
        index_col=["name", "date"],
    )

    return data

@st.cache_data
def plot_cumulative_returns(data, title, x_label, y_label, color='name'):
    fig = px.line(data.reset_index(), x=x_label, y=y_label, color=color, title=title)
    return fig

sp500_data = load_sp500_data()
congress_data = load_congress_data()
insider_data = load_insider_data()

sp500_cut = sp500_data.loc["2020-01-01":].copy()
sp500_cut["cum_return"] = (1 + sp500_cut["daily_return"]).cumprod() - 1

congress_cut = congress_data.loc["2020-01-01":].copy()
congress_cut["cum_return"] = (1 + congress_cut["return"]).groupby("name").cumprod() - 1

# insider data 20
insider_cut = insider_data.loc["2020-01-01":].copy()
insider_cut["cum_return"] = (1 + insider_cut["return"]).groupby("name").cumprod() - 1

# Remove outlier
congress_cut = congress_cut.drop("Donald S. Beyer, Jr.", level="name")

# Calculating and plotting average cumulative returns for all Congress members
congress_avg_cum_returns = congress_cut.groupby('date')['cum_return'].mean().reset_index()

# Merging both dataframes on date for comparison
merged_data = pd.merge(sp500_cut, congress_avg_cum_returns, on='date', suffixes=('_sp500', '_congress'))

# Plotting cumulative returns
fig = plot_cumulative_returns(merged_data, 'Cumulative Returns: S&P 500 vs Congress', 'date', ['cum_return_sp500', 'cum_return_congress'], 'variable')
fig.for_each_trace(lambda t: t.update(name='S&P 500' if t.name == 'cum_return_sp500' else 'Congress Average'))

# Change variable to series
fig.update_layout(
    yaxis_title='Cumulative Return',
    xaxis_title='Date',
)
if st.sidebar.checkbox("Show Insider Trading Data", value=True):
    # Adding insider trading data
    insider_avg_cum_returns = insider_cut.groupby('date')['cum_return'].mean().reset_index()
    insider_avg_cum_returns = insider_avg_cum_returns[insider_avg_cum_returns['date'] >= '2020-01-01']
    fig.add_scatter(x=insider_avg_cum_returns['date'], y=insider_avg_cum_returns['cum_return'], mode='lines', name='Insider Flagged Average')

# if checked in the sidebar:
if st.sidebar.checkbox("Show Top 10 Insider Traders", value=True):
    # Calculating top 10 insider traders
    top_10_insider = insider_cut.groupby('name')['cum_return'].last().sort_values(ascending=False).head(10)
    top_10_insider_avg_cum_returns = insider_cut[insider_cut.index.get_level_values('name').isin(top_10_insider.index)]
    top_10_insider_avg_cum_returns = top_10_insider_avg_cum_returns.groupby('date')['cum_return'].mean().reset_index()
    top_10_insider_avg_cum_returns = top_10_insider_avg_cum_returns[top_10_insider_avg_cum_returns['date'] >= '2020-01-01']

    # Adding top 10 insider traders average cumulative returns
    fig.add_scatter(x=top_10_insider_avg_cum_returns['date'], y=top_10_insider_avg_cum_returns['cum_return'], mode='lines', name='Top 10 Insider Average')

# if checked in the sidebar:
if st.sidebar.checkbox("Show Top 50 Congress Members", value=True):
    # Adding top 50 congress members average cumulative returns
    top_50_congress = congress_cut.groupby('name')['cum_return'].last().sort_values(ascending=False).head(50)
    top_50_congress_avg_cum_returns = congress_cut[congress_cut.index.get_level_values('name').isin(top_50_congress.index)]
    top_50_congress_avg_cum_returns = top_50_congress_avg_cum_returns.groupby('date')['cum_return'].mean().reset_index()
    top_50_congress_avg_cum_returns = top_50_congress_avg_cum_returns[top_50_congress_avg_cum_returns['date'] >= '2020-01-01']
    fig.add_scatter(x=top_50_congress_avg_cum_returns['date'], y=top_50_congress_avg_cum_returns['cum_return'], mode='lines', name='Top 50 Congress Average')

# full_width
st.plotly_chart(fig, use_container_width=True)


row1_1, row1_2, row1_3 = st.columns((1, 1, 2.5))

with row1_1:
    # show the top 50 congress members
    st.write("**Top 50 Congress Members**")
    st.write(top_50_congress)

with row1_2:
    # show the top insider traders
    st.write("**Top 10 Insider Traders**")
    st.write(top_10_insider)

with row1_3:
    # show all insider trades
    st.write("**Insider Trading Data**")
    st.write(insider_cut)
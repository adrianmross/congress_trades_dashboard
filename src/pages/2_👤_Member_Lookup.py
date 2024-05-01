from cProfile import label
import os
from tkinter import Place
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Member Lookup", 
                   page_icon="👤",
                   layout="wide",
                   )

st.markdown("# Congress Member Lookup")
st.sidebar.header("Plotting")
st.write(
    """
    This page allows you to search for a specific Congress member and view their returns.
    """
)

# Load S&P500 data
@st.cache_resource
def load_sp500_data():
    path = "s%26p500_returns.csv.gz"
    if not os.path.exists(path):
        path = f"https://github.com/adrianmross/congress_trades_dashboard/raw/main/data/outputs/{path}"
    data = pd.read_csv(path, parse_dates=["date"], index_col="date")
    return data

# Load Congress returns data
@st.cache_resource
def load_congress_data():
    path = "congress_returns.csv.gz"
    if not os.path.exists(path):
        path = f"https://github.com/adrianmross/congress_trades_dashboard/raw/main/data/outputs/{path}"
    data = pd.read_csv(path, parse_dates=["date"], index_col=["name", "date"])
    return data

# Function to plot cumulative returns
@st.cache_data
def plot_cumulative_returns(data, title, x_label, y_label, color=None):
    if color:
        fig = px.line(data.reset_index(), x=x_label, y=y_label, color=color, title=title)
    else:
        fig = px.line(data, x=x_label, y=y_label, title=title)
    return fig

# FILTER DATA FOR A SPECIFIC MEMBER, CACHE
@st.cache_data
def filterdata(df, member_selected):
    return df[df.index.get_level_values('name') == member_selected]

sp500_data = load_sp500_data()
congress_data = load_congress_data()

sp500_cut = sp500_data.loc["2020-01-01":].copy()
sp500_cut["cum_return"] = (1 + sp500_cut["daily_return"]).cumprod() - 1

congress_cut = congress_data.loc["2020-01-01":].copy()
congress_cut["cum_return"] = (1 + congress_cut["return"]).groupby("name").cumprod() - 1
congress_cut = congress_cut.drop("Donald S. Beyer, Jr.", level="name")

# Autocomplete search feature
congress_names = congress_cut.index.get_level_values('name').unique()

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((1, 2.5))

with row1_1:
    # show a dataframe of the congress members ranked by best cumulative return
    st.write("**Highest Cumulative Return Ranking**")
    ranking = congress_cut.groupby("name")["cum_return"].last().sort_values(ascending=False).copy()
    ranking = ranking.reset_index().rename(columns={"name": "Member"}).drop(columns="cum_return")
    ranking.index = range(1, len(ranking)+1)
    ranking.index.name = "Rank"
    st.write(ranking)



with row1_2:
    # search_query = st.selectbox("Search for a Congress member", options=congress_names, format_func=lambda x: x)
    # blank option for search
    search_query = st.selectbox("Search for a Congress member", 
                                congress_names, 
                                format_func=lambda x: x,
                                index=None,)

    # Save member name to cache
    if st.session_state.get("member_name") is None:
        st.session_state.member_name = search_query

    if search_query is not None:
        congress_member_data =  filterdata(congress_cut, search_query)

        # Plotting the cumulative returns
        fig = px.line(congress_member_data.reset_index(), x="date", y="cum_return", 
                    title=f"{search_query} Cumulative Returns", labels={"cum_return": "Cumulative Return", "date": "Date"},
                        color="name")
        # rename title in legend to "series"
        fig.update_layout(legend_title_text="Series")
        # Add S&P500 data to the plot
        fig.add_scatter(x=sp500_cut.index, y=sp500_cut["cum_return"], mode="lines", name="S&P 500")
        
    else :
        fig = px.line(congress_cut.reset_index(), x="date", y="cum_return", 
                    title=f"Congress Cumulative Returns", labels={"cum_return": "Cumulative Return", "date": "Date"},
                        color="name")
        fig.update_layout(legend_title_text="Member")

    st.plotly_chart(fig)
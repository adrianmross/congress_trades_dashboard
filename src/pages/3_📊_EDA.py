import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="EDA", 
    page_icon="📊",
    layout="wide",)

st.markdown("# Exploratory Data Analysis")

@st.cache_resource
def load_purchase_data():
    path = "purchase_impact.csv"
    if not os.path.exists(path):
        path = f"https://github.com/adrianmross/congress_trades_dashboard/raw/main/data/outputs/{path}"
    data = pd.read_csv(path)
    return data

@st.cache_resource
def load_selling_data():
    path = "sell_impact.csv"
    if not os.path.exists(path):
        path = f"https://github.com/adrianmross/congress_trades_dashboard/raw/main/data/outputs/{path}"
    data = pd.read_csv(path)
    return data

# purchase_impact schema: ticker,daily_return,trading_days_before_after,disclosure_date,sector,cum_return,date,adjclose

purchase_data = load_purchase_data()
selling_data = load_selling_data()

# filter by sector and then group by trading days before/after

# choose sector
sectors = purchase_data["sector"].unique()
sector = st.sidebar.selectbox("Choose a sector", sectors)

# filter data
purchase_sector_data = purchase_data[purchase_data["sector"] == sector]
selling_sector_data = selling_data[selling_data["sector"] == sector]

# group by trading days before/after
purchase_sector_grouped = purchase_sector_data.groupby("trading_days_before_after")['daily_return'].mean()
selling_sector_grouped = selling_sector_data.groupby("trading_days_before_after")['daily_return'].mean()

# plot
fig = px.line(purchase_sector_grouped.reset_index(), x='trading_days_before_after', y='daily_return', title=f"Purchase Impact on {sector} Stocks")
st.plotly_chart(fig)

fig = px.line(selling_sector_grouped.reset_index(), x='trading_days_before_after', y='daily_return', title=f"Selling Impact on {sector} Stocks")
st.plotly_chart(fig)




from email.mime import image
from logging import info
import os
import pandas as pd
import numpy as np
import streamlit as st
import wikipedia as wp
import requests
import bs4
import plotly.express as px

st.set_page_config(page_title="Member Lookup", 
                   page_icon="👤",
                   layout="wide",
                   )

st.markdown("# Congress Member Lookup")
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

@st.cache_resource
def load_trades_data():
    path = "transactions.csv"
    if not os.path.exists(path):
        path = f"https://github.com/adrianmross/congress_trades_dashboard/raw/main/data/inputs/{path}"
    data = pd.read_csv(path)
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
trades_data = load_trades_data()

sp500_cut = sp500_data.copy()
congress_cut = congress_data.copy()

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

        # Get earliest date for the member
        earliest_date = congress_member_data.index.get_level_values('date').min()

        # Filter S&P500 data to match the earliest date for the member
        sp500_cut = sp500_cut.loc[earliest_date:].copy()
        sp500_cut["cum_return"] = (1 + sp500_cut["daily_return"]).cumprod() - 1

        # Plotting the cumulative returns
        fig = px.line(congress_member_data.reset_index(), x="date", y="cum_return", 
                    title=f"{search_query} v. S&P500 Cumulative Returns", labels={"cum_return": "Cumulative Return", "date": "Date"},
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

def get_info_dict(page):
    response = requests.get(page.url)
    soup = bs4.BeautifulSoup(response.text, 'html')
    infobox = soup.find('table', {'class': 'infobox'})
    return infobox

def get_image_from_infobox(infobox):
    image = info_dict.find('img')['src']
    return "https:"+image

if search_query is not None:
    st.write("### Member Details")

    row2_1, row2_2, row2_3 = st.columns((1.25, 2, 3))
    
    try:
        result = wp.search("Congress member" + search_query, results=1)
        page = wp.page(result[0])
    except:
        pass

    with row2_1:
        try:
            info_dict = get_info_dict(page)
            image = get_image_from_infobox(info_dict)
            st.image(image, use_column_width=True)
            df = pd.read_html(str(info_dict))[0].copy()
        except:
            st.write("No information found for this member.")
            # df = pd.DataFrame()

        st.write(f"### {search_query}")

        try:
            # political party
            political_party_row_index = df[df.iloc[:, 0].str.contains('Political party', na=False)].index[0]
            political_party = df.iloc[political_party_row_index, 1]
            st.write(f"**Political Party:** {political_party}")
        except:
            st.write("Political party not found.")

    with row2_2:
        try:
            st.write("#### Biography")
            st.write(wp.summary("Congress member" + search_query, sentences=4))
        except:
            pass

    with row2_3:
        # get list of trades
        trades = trades_data[trades_data["name"] == search_query].copy()
        st.write("#### Recent Trades")
        st.write(trades)


    # st.write(df)




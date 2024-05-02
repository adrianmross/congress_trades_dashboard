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

@st.cache_resource
def load_trades_data():
    path = "transactions.csv"
    if not os.path.exists(path):
        path = f"https://github.com/adrianmross/congress_trades_dashboard/raw/main/data/inputs/{path}"
    data = pd.read_csv(
        path,
        parse_dates=["transaction_date"],
        )
    return data

purchase_data = load_purchase_data()
selling_data = load_selling_data()
trades_data = load_trades_data()

# choose sector
sectors = purchase_data["sector"].unique()
st.sidebar.header("Disclosure Impact Analysis")
sector = st.sidebar.selectbox("Choose a sector", sectors)

# filter data
purchase_sector_data = purchase_data[purchase_data["sector"] == sector]
selling_sector_data = selling_data[selling_data["sector"] == sector]

# group by trading days before/after
purchase_sector_grouped = purchase_sector_data.groupby("trading_days_before_after")['daily_return'].mean()
selling_sector_grouped = selling_sector_data.groupby("trading_days_before_after")['daily_return'].mean()

st.write(
    """
    ## Impact of Purchases and Sales on Stock Returns

    The visualizations demonstrate the average daily returns on stocks before and after purchase and selling 
    activities within a chosen sector, revealing potential trends or anomalies in price movements related to 
    transaction timings.
    """
)

chart_buy_sell = st.sidebar.radio("Select data to display:", ("Purchase", "Sale"))

if chart_buy_sell == "Purchase":
    fig = px.line(purchase_sector_grouped.reset_index(), x='trading_days_before_after', y='daily_return', 
                title=f"Purchase Impact on {sector} Stocks", color_discrete_sequence=['teal'],
                labels={'trading_days_before_after': 'Trading Days Before/After', 'daily_return': 'Average Daily Return'})
    st.plotly_chart(fig)

else:
    fig = px.line(selling_sector_grouped.reset_index(), x='trading_days_before_after', y='daily_return', 
                title=f"Selling Impact on {sector} Stocks", color_discrete_sequence=['#EF553B'],
                labels={'trading_days_before_after': 'Trading Days Before/After', 'daily_return': 'Average Daily Return'})
    st.plotly_chart(fig)

st.write(
    """
    ## Transaction Frequency Over Time

    This interactive line chart illustrates the frequency of financial transactions over time. The X-axis represents 
    the dates of transactions, and the Y-axis indicates the number of transactions per date. Peaks in the line denote 
    days with higher activity, highlighting trends and anomalies in transaction volume across the observed period.
    """
)

options = ["Transaction Frequency", "Purchase vs Sale", "Democrat vs Republican"]
st.sidebar.header("Transaction Frequency Analysis")
chart_type = st.sidebar.selectbox("Select chart type:", options, index=0)

if chart_type == "Transaction Frequency":
    # Count the number of transactions per date and reset index for plotting
    transaction_counts_df = trades_data['transaction_date'].value_counts().sort_index().reset_index()
    transaction_counts_df.columns = ['transaction_date', 'counts']

    # Create the interactive plot
    fig = px.line(transaction_counts_df, x='transaction_date', y='counts', title='Frequency of Transactions Over Time',
                labels={'transaction_date': 'Date', 'counts': 'Number of Transactions'})
    st.plotly_chart(fig)

elif chart_type == "Purchase vs Sale":
    # Categorize each transaction as 'purchase' or 'sale'
    transactions_data_2 = trades_data.copy()
    transactions_data_2['transaction_category'] = transactions_data_2['type'].apply(lambda x: 'purchase' if 'purchase' in x else 'sale')

    # Aggregate data by date and transaction category
    transaction_category_counts = transactions_data_2.groupby(['transaction_date', 'transaction_category']).size().unstack(fill_value=0).reset_index()

    # Create the interactive stacked bar chart
    fig = px.bar(transaction_category_counts, x='transaction_date', y=['purchase', 'sale'],
                title='Frequency of Transactions Over Time (Purchases vs. Sales)',
                labels={'value': 'Number of Transactions', 'transaction_date': 'Date'},
                color_discrete_map={'purchase': 'teal', 'sale': '#EF553B'},  # Optional: custom color mapping
                )
    fig.update_layout(barmode='stack')

    st.plotly_chart(fig)

else:
    # Add a column categorizing transactions as Democrat or Republican
    transactions_data_3 = trades_data.copy()
    transactions_data_3['party_category'] = transactions_data_3['party'].apply(lambda x: 'Democrat' if x == 'Democrat' else ('Republican' if x == 'Republican' else 'Other'))

    # Aggregate data by date and party category
    party_category_counts = transactions_data_3.groupby(['transaction_date', 'party_category']).size().unstack(fill_value=0).reset_index()

    # Create the interactive stacked bar chart
    fig = px.bar(party_category_counts, x='transaction_date', y=['Democrat', 'Republican'],
                title='Frequency of Transactions Over Time by Political Party',
                labels={'value': 'Number of Transactions', 'transaction_date': 'Date'},
                color_discrete_map={'Democrat': '#1F77B4', 'Republican': '#DC3912'},  # Custom color mapping for parties
                height=400)
    fig.update_layout(barmode='stack', bargap=0.2)  # Adjust bargap to change spacing

    st.plotly_chart(fig)

def convert_amount_range_to_midpoint(amount_range):
    try:
        # Remove dollar signs and commas, check for empty or invalid entries
        amount_range = amount_range.replace('$', '').replace(',', '').strip()
        if '-' not in amount_range or not amount_range:
            return None  # Skip empty, malformed, or missing ranges
        
        # Split the range into lower and upper bounds
        lower, upper = amount_range.split('-')
        # Convert bounds to float and calculate midpoint
        return (float(lower.strip()) + float(upper.strip())) / 2
    except Exception as e:
        # st.error(f"Error processing amount range: {e}")
        return None

# Sidebar option for selecting the chart type
st.write(
    """
    ## Transaction Data Analysis

    The following visualizations provide insights into the distribution of transaction types, amounts, industries, 
    and states. These charts offer a comprehensive overview of the transaction data, highlighting key trends and 
    patterns in the financial activities of congress members.
    """
)
options = ["Transaction Type Distribution", "Transaction Amount Distribution (Log)", "Top 10 Industries by Number of Transactions", "Top 10 States by Number of Transactions"]
st.sidebar.header("Transaction Data Analysis")
chart_type = st.sidebar.selectbox("Select chart type:", options, index=0)

if chart_type == "Transaction Type Distribution":
    # Transaction Type Distribution
    transaction_types = trades_data['type'].value_counts().reset_index()
    transaction_types.columns = ['Transaction Type', 'Count']  # Correctly rename columns for clarity
    fig = px.pie(transaction_types, values='Count', names='Transaction Type', title='Transaction Type Distribution')
    st.write("""
        #### Transaction Type Distribution  
        This chart shows the distribution of different types of transactions.
        """
    )
    st.plotly_chart(fig)

elif chart_type == "Transaction Amount Distribution (Log)":
    # Transaction Amount Distribution with Log Scale
    trades_data['amount_midpoint'] = trades_data['amount'].apply(convert_amount_range_to_midpoint)
    trades_data['log_amount'] = np.log10(trades_data['amount_midpoint'] + 1)  # Log transform the midpoint value
    fig = px.histogram(trades_data, x='log_amount', title='Transaction Amount Distribution (Log Scale)')
    st.write(
        """
        #### Transaction Amount Distribution (Log Scale)
        This histogram shows the distribution of transaction amounts on a logarithmic scale to highlight variations across different magnitudes.
        """
    )
    st.plotly_chart(fig)

elif chart_type == "Top 10 Industries by Number of Transactions":
    # Transactions by Industry
    industry_counts = trades_data['industry'].value_counts().nlargest(10).reset_index()
    industry_counts.columns = ['Industry', 'Transactions']
    fig = px.bar(industry_counts, x='Industry', y='Transactions', title='Top 10 Industries by Number of Transactions')
    st.write(
        """
        #### Top 10 Industries by Number of Transactions
        This bar chart ranks the top 10 industries by the number of transactions recorded.
        """
    )
    st.plotly_chart(fig)

elif chart_type == "Top 10 States by Number of Transactions":
    # Transactions by State
    state_counts = trades_data['state'].value_counts().nlargest(10).reset_index()
    state_counts.columns = ['State', 'Transactions']
    fig = px.bar(state_counts, x='State', y='Transactions', title='Top 10 States by Number of Transactions')
    st.write(
        """
        #### Top 10 States by Number of Transactions
        This bar chart shows the states with the highest number of transactions.
        """
    )
    st.plotly_chart(fig)
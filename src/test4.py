import pandas as pd

# Sample data for transactions
transactions = {
    'Date': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-01', '2023-01-03', '2023-01-04', '2023-01-02', '2023-01-03'],
    'Name': ['Alice', 'Alice', 'Alice', 'Alice', 'Bob', 'Bob', 'Bob', 'Charlie', 'Charlie'],
    'Ticker': ['AAPL', 'GOOGL', 'AAPL', 'AAPL', 'GOOGL', 'GOOGL', 'MSFT', 'AAPL', 'GOOGL'],
    'Type': ['buy', 'buy', 'buy', 'sell', 'buy', 'sell', 'buy', 'buy', 'sell'],
    'Shares': [10, 3, 5, 3, 20, 10, 15, 8, 5],
    'Price': [150, 1000, 152, 155, 1000, 1010, 300, 150, 1010]
}

df = pd.DataFrame(transactions)
df['Date'] = pd.to_datetime(df['Date'])

# Calculate cost and adjust for buys/sells
df['Transaction Value'] = df['Shares'] * df['Price']
df.loc[df['Type'] == 'sell', 'Shares'] = -df['Shares']
df.loc[df['Type'] == 'sell', 'Transaction Value'] = -df['Transaction Value']

# Assuming daily closing prices for the stocks
closing_prices = {
    'AAPL': {pd.Timestamp('2023-01-01'): 150, pd.Timestamp('2023-01-02'): 152, pd.Timestamp('2023-01-03'): 155, pd.Timestamp('2023-01-04'): 153},
    'GOOGL': {pd.Timestamp('2023-01-01'): 1000, pd.Timestamp('2023-01-02'): 1005, pd.Timestamp('2023-01-03'): 1010, pd.Timestamp('2023-01-04'): 1020},
    'MSFT': {pd.Timestamp('2023-01-01'): 300, pd.Timestamp('2023-01-02'): 305, pd.Timestamp('2023-01-03'): 310, pd.Timestamp('2023-01-04'): 315}
}

# Convert to DataFrame and reset index for easy merge
prices_df = pd.DataFrame(closing_prices).stack().reset_index()
prices_df.columns = ['Date', 'Ticker', 'Price']
prices_df['Date'] = pd.to_datetime(prices_df['Date'])

# Create a comprehensive DataFrame for all dates
dates = pd.date_range(start=df['Date'].min(), end=df['Date'].max())
names = df['Name'].unique()
tickers = df['Ticker'].unique()

# Create a multi-index DataFrame with all combinations
full_index = pd.MultiIndex.from_product([dates, names, tickers], names=['Date', 'Name', 'Ticker'])
full_df = pd.DataFrame(index=full_index).reset_index()

# Merge prices into full_df
full_df = full_df.merge(prices_df, on=['Date', 'Ticker'], how='left')

# Merge transactions into full_df
full_df = full_df.merge(df, on=['Date', 'Name', 'Ticker'], how='inner')
full_df.fillna({'Shares': 0, 'Transaction Value': 0, 'Price': 0}, inplace=True)

# Cumulative calculations for shares and investment
full_df['Cumulative Shares'] = full_df.groupby(['Name', 'Ticker'])['Shares'].cumsum()
full_df['Cumulative Investment'] = full_df.groupby(['Name', 'Ticker'])['Transaction Value'].cumsum()

# Calculate daily values
full_df['Daily Value'] = full_df['Cumulative Shares'] * full_df['Price_y']

full_df['Previous Day Value'] = full_df.groupby(['Name', 'Ticker'])['Daily Value'].shift(1)
full_df['Daily Return'] = (full_df['Daily Value'] - full_df['Transaction Value'] - full_df['Previous Day Value']) / full_df['Previous Day Value']
                            # 1860 - - 465 - 2280.0 = 1860 + 465 = 2325 - 2280 = 45
full_df['Daily Return'].fillna(0, inplace=True)

print(full_df)
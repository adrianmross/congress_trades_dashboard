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

# # Calculate cumulative return
# full_df['Cumulative Return'] = (full_df['Daily Value'] - full_df['Cumulative Investment']) / full_df['Cumulative Investment'].where(full_df['Cumulative Investment'] != 0, 1)
# (Daily Value_n - (Daily Value_n-1 + Cash_Flow_n)) / (Daily Value_n-1 + Cash_Flow_n)
# full_df['Time_Weighted Return'] = (full_df['Daily Value'] - full_df['Cumulative Investment']) / (full_df['Cumulative Investment'] + full_df['Transaction Value'])
# print(full_df)

# for each person, day calculate the total value of the total portfolio
full_df['Daily Portfolio Value'] = full_df.groupby(['Name', 'Date'])['Daily Value'].transform('sum')

# do a rolling sum of the total portfolio value (make sure we only sum once per day)
total_port_value_df = full_df.groupby(['Name', 'Date'])['Daily Portfolio Value'].first().groupby('Name').cumsum()
# label the column
total_port_value_df = total_port_value_df.reset_index()
total_port_value_df.columns = ['Name', 'Date', 'Total Portfolio Value']

# merge the total portfolio value back into the full dataframe
full_df = full_df.merge(total_port_value_df, on=['Name', 'Date'], how='left')

# weight of each asset in the portfolio
full_df['Weight'] = full_df['Daily Value'] / full_df['Total Portfolio Value']

# full_df['Previous Day Value'] = full_df.groupby(['Name', 'Ticker'])['Daily Value'].shift(1)
# full_df['Daily Return'] = (full_df['Daily Value'] - full_df['Previous Day Value']) / full_df['Previous Day Value']
# full_df['Daily Return'].fillna(0, inplace=True)

# calculate realized and unrealized returns
# full_df['Realized Return'] = full_df['Cumulative Investment'] / full_df['Transaction Value']

# # for each person, day calculate the running total portfolio across assets
# full_df['Running Portfolio Value'] = full_df.groupby(['Name'])['Total Portfolio Value'].cumsum()
# this has error becuase its grabbing total portfolio value twice on the same day
# need to fix this


# # # Calculate realized gains
# full_df['Realized Gains'] = full_df['Daily Value'] - full_df['Cumulative Investment']

print(full_df)

# # Calculate regular return (including both realized and unrealized gains)
# full_df['Regular Return'] = (full_df['Daily Value'] / full_df.groupby(['Name', 'Ticker'])['Transaction Value'].cumsum()) - 1

# # Step 1: Calculate the daily value of each asset in the portfolio
# full_df['Daily Asset Value'] = full_df['Cumulative Shares'] * full_df['Price_y'] + full_df['Realized Gains']

# # Step 2: Sum up the daily values of all assets for each day to get the total portfolio value
# portfolio_daily_value = full_df.groupby(['Date', 'Name'])['Daily Asset Value'].sum().reset_index()

# # Step 3: Calculate the daily returns of the portfolio
# portfolio_daily_value['Portfolio Daily Return'] = portfolio_daily_value.groupby('Name')['Daily Asset Value'].pct_change()

# # Step 4: Cumulatively multiply the daily returns to get the cumulative return of the portfolio
# portfolio_daily_value['Cumulative Portfolio Return'] = (1 + portfolio_daily_value.groupby('Name')['Portfolio Daily Return'].fillna(0)).cumprod() - 1

# print(portfolio_daily_value)

# Aggregate to get total return by person
# total_return = full_df.groupby(['Name', 'Date'])['Regular Return'].prod().reset_index()
# print(total_return)

# print full_df where Name is Alice
# print(full_df[full_df['Name'] == 'Bob'])
# # Aggregate to get total return by person
# total_return = full_df.groupby(['Name', 'Date'])['Cumulative Return'].sum().reset_index()
# print(total_return)

# Select the final DataFrame to display
# output_df = full_df[['Date', 'Name', 'Ticker', 'Daily Value', 'Cumulative Return']]
# print(output_df)

import pandas as pd

# Transactions Data
data = {
    'transaction_date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-01', '2023-01-03', '2023-01-04', '2023-01-02', '2023-01-03'],
    'name': ['Alice', 'Alice', 'Alice', 'Bob', 'Bob', 'Bob', 'Charlie', 'Charlie'],
    'ticker': ['AAPL', 'AAPL', 'AAPL', 'GOOGL', 'GOOGL', 'MSFT', 'AAPL', 'GOOGL'],
    'type': ['buy', 'buy', 'sell', 'buy', 'sell', 'buy', 'buy', 'sell'],
    'amount': [10, 5, 3, 20, 10, 15, 8, 5]
}

prices = {
    'AAPL': {pd.Timestamp('2023-01-01'): 150, pd.Timestamp('2023-01-02'): 152, pd.Timestamp('2023-01-03'): 155, pd.Timestamp('2023-01-04'): 153},
    'GOOGL': {pd.Timestamp('2023-01-01'): 1000, pd.Timestamp('2023-01-02'): 1005, pd.Timestamp('2023-01-03'): 1010, pd.Timestamp('2023-01-04'): 1020},
    'MSFT': {pd.Timestamp('2023-01-01'): 300, pd.Timestamp('2023-01-02'): 305, pd.Timestamp('2023-01-03'): 310, pd.Timestamp('2023-01-04'): 315}
}

df = pd.DataFrame(data)
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

# Creating a full date range for the period in the data
date_range = pd.date_range(start=df['transaction_date'].min(), end=df['transaction_date'].max())

# Expand prices to include all dates
expanded_prices = []
for ticker, dates in prices.items():
    ticker_prices = pd.Series(dates).reindex(date_range, method='ffill').to_frame('price')
    ticker_prices['ticker'] = ticker
    ticker_prices.reset_index(inplace=True)
    ticker_prices.rename(columns={'index': 'date'}, inplace=True)
    expanded_prices.append(ticker_prices)

prices_df = pd.concat(expanded_prices)

# Merge transactions with expanded prices
df = pd.merge(df, prices_df, left_on=['transaction_date', 'ticker'], right_on=['date', 'ticker'])

# Adjust amounts for transaction type
df['adjusted_amount'] = df.apply(lambda x: x['amount'] if x['type'] == 'buy' else -x['amount'], axis=1)

# Calculate cumulative shares
df['cumulative_shares'] = df.groupby(['name', 'ticker'])['adjusted_amount'].cumsum()

# Project holdings forward on all dates for all tickers each person holds
portfolio = df.groupby(['name', 'ticker', 'date']).agg({'cumulative_shares': 'last', 'price': 'last'})
portfolio.reset_index(inplace=True)

# Full projection of holdings across all dates
portfolio_full = pd.DataFrame(index=pd.MultiIndex.from_product([portfolio['name'].unique(), portfolio['ticker'].unique(), date_range], names=['name', 'ticker', 'date']))
portfolio_full = portfolio_full.join(portfolio.set_index(['name', 'ticker', 'date']), how='left').fillna(method='ffill')

# Calculate daily portfolio values
portfolio_full['daily_value'] = portfolio_full['cumulative_shares'] * portfolio_full['price']

# Aggregate to get total value by person per day
total_daily_values = portfolio_full.groupby(['name', 'date'])['daily_value'].sum()

# Calculate cumulative return based on the initial value
initial_values = total_daily_values.groupby('name').transform('first')
cumulative_returns_by_day = ((total_daily_values - initial_values) / initial_values * 100).reset_index()
cumulative_returns_by_day.columns = ['name', 'date', 'cumulative_return']

print(cumulative_returns_by_day)

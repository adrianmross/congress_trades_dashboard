import pandas as pd

# Sample transaction data
data = {
    'transaction_date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-01', '2023-01-03', '2023-01-04', '2023-01-02', '2023-01-03'],
    'name': ['Alice', 'Alice', 'Alice', 'Bob', 'Bob', 'Bob', 'Charlie', 'Charlie'],
    'ticker': ['AAPL', 'AAPL', 'AAPL', 'GOOGL', 'GOOGL', 'MSFT', 'AAPL', 'GOOGL'],
    'type': ['buy', 'buy', 'sell', 'buy', 'sell', 'buy', 'buy', 'sell'],
    'amount': [10, 5, 3, 20, 10, 15, 8, 5]
}

# Sample price data
prices = {
    'AAPL': {pd.Timestamp('2023-01-01'): 150, pd.Timestamp('2023-01-02'): 152, pd.Timestamp('2023-01-03'): 155, pd.Timestamp('2023-01-04'): 153},
    'GOOGL': {pd.Timestamp('2023-01-01'): 1000, pd.Timestamp('2023-01-02'): 1005, pd.Timestamp('2023-01-03'): 1010, pd.Timestamp('2023-01-04'): 1020},
    'MSFT': {pd.Timestamp('2023-01-01'): 300, pd.Timestamp('2023-01-02'): 305, pd.Timestamp('2023-01-03'): 310, pd.Timestamp('2023-01-04'): 315}
}

# Create a DataFrame from transaction data
df = pd.DataFrame(data)
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

# Creating a DataFrame from prices data
price_list = []
for ticker, days in prices.items():
    for date, price in days.items():
        price_list.append({'transaction_date': date, 'ticker': ticker, 'price': price})
prices_df = pd.DataFrame(price_list)

# Merge transactions with prices
df = pd.merge(df, prices_df, on=['transaction_date', 'ticker'], how='left')

# Adjust amounts for transaction type
df['adjusted_amount'] = df.apply(lambda x: x['amount'] if x['type'] == 'buy' else -x['amount'], axis=1)

# Calculate cumulative holdings
df['cumulative_shares'] = df.groupby(['name', 'ticker'])['adjusted_amount'].cumsum()

# Calculate the value of the current holdings
df['current_value'] = df['cumulative_shares'] * df['price']

# Initial and final investment calculations
initial_investment = df.groupby(['name', 'ticker']).apply(lambda x: x.iloc[0]['cumulative_shares'] * x.iloc[0]['price'])
final_investment = df.groupby(['name', 'ticker']).apply(lambda x: x.iloc[-1]['current_value'])

# Calculate cumulative returns
cumulative_return = ((final_investment - initial_investment) / initial_investment) * 100

# Prepare the final DataFrame
cumulative_return = cumulative_return.reset_index()
cumulative_return.columns = ['name', 'ticker', 'cumulative return (%)']

print(cumulative_return)

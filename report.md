# Project Purpose and Appendix

## Introduction/Motivation

Public trust in government officials has been steadily declining.  Data from the Pew Research Center 
shows a dramatic drop in public trust from 44% in 2000 to just 16%.[^1] This 28% decrease has been 
influenced by numerous factors, including prolonged conflicts in the Middle East, China's ascent in power, 
and contentious presidential elections.  However, a significant contributor to this erosion of trust is the 
ability of Congress members to trade stocks.  In fact, a 2022 survey by Business Insider revealed that 70% of 
likely voters favor a complete ban on stock trading by lawmakers.[^2]

In response to growing concerns, Congress enacted the STOCK Act in 2012, which mandates that lawmakers 
disclose their stock trades.  However, the legislation has significant shortcomings.  For instance, 
disclosures are only required 45 days post-transaction, and the penalty for non-compliance is a nominal 
$200 fine, doing little to curb stock trading among legislators. 

Our project aims to cast a spotlight on congressional stock trades.  We investigate whether 
lawmakers achieve abnormally high returns, if their political affiliation influences their trading decisions, 
and whether the committees they serve on impact their investment choices in specific industries.
    

## Hypotheses and Research Proposal

In this research, we explore the relationship between trading activities we have classified as insider trading 
by Congress members and the performance of the stocks involved. We will test the following hypotheses:

1. Congressional insider trading will consistently outperform the S&P 500. 
2. The disclosure of trading activities by members of certain committees exerts varied impacts on stock performance. 
Specifically, committees associated with finance, healthcare, and technology wield a pronounced influence on the stocks 
they trade, resulting in notable price fluctuations following the revelation of such activities.

**Read more on the initial proposal [here](https://github.com/adrianmross/congress_trades_dashboard/blob/main/proposal.md).**


## Data Collection

Below are the details of how we get the data. All the csv files mentioned below are in data/inputs/ folder and all 
the Jupyter Notebook files are in src/getters/.

### Congress Transactions Data

`transactions.csv` and `get_congress_trans.ipynb`: As mentioned in our proposal, we collect the data on Congressional 
transactions from [Senate Stock Watcher](https://senatestockwatcher.com/api) and [House Stock Watcher APIs](https://housestockwatcher.com/api). 
To clean up the data, we:

- Replace the typos for `transaction_date` column manually such as `0009-06-09` to `2021-06-09` or `0022-11-23` to 
`2022-11-23` based on the disclosure date. We do this because `transaction_date` is usually close to `disclosure_date` 
with 1-2 month gap between them as Congressional people are obliged to disclose their transaction date within 30-45 days.
- Due to the lack of data (with respect to being able to calculate the derivative's return), we dropped any transactions 
that deal with options
- Drop rows that have ticker as null values
- Drop all other columns except for `disclosure_date`, `transaction_date`, `ticker`, `type`, `amount`, `name`, 
`asset_description`, `state`, `party`, `industry`, `sector`, which are relevant to our analysis
- Merge House and Senate transactions into one data frame
- Change `transaction_type` to the same format: lowercase and has 3 possible values: `sale_partial`, `sale_full`, 
and `purchase`. Again for the simplicity of our project, we drop transactions whose type is exchange

### S&P500 Returns Data

`s&p500_returns.csv` and `get_stock_prices.ipynb`: We chose the ticker `^GSPC` as our S&P500 index. 
We then use `yahoo_fin` Python library to help use pull the stock's daily adjusted closing prices starting from Jan 1 2024 
to April 29 2024.  Then we calculate daily returners using pct_change and cumulative returns using `cumprod`and fill in NA 
values with 0.  

### Committee Data

`get_house_data.ipynb` and `get_senate_data.ipynb`, with `house_committees.csv` and `senators_committees.csv`, are the scripts 
and their resulting generated data files for capturing details on Congress members. They involved scraping two government websites: 
[House.gov](https://www.house.gov/representatives) and [Senate.gov](https://www.senate.gov/general/committee_assignments/assignments.htm)
to get the official names of the 118th Congress and their committee assignments. We needed additional data for Senators (party and state), 
which involved scraping Wikipedia. The merging of these sources for Senators posed a challenge due to irregularities in naming 
(nicknames, format, the inclusion/exclusion of middle or additional names).

### Industry Data

`committee_gic_mapping.csv` contained the mappings of Congress committees to Industry sectors (`gsectors`). We found no good resource 
on a direct mapping and therefore relied on our interpretation of the committees' missions and business interactions.

## Data Processing

### Calculating Returns

#### Calculation of Cumulative Returns
1. **Average Transaction Amount**: For transactions specifying a range of values (e.g., $1,001 - $15,000), an average amount was calculated by taking the midpoint of the specified range. This provided a standardized value for each transaction, aiding in more accurate portfolio valuation.

2. **Stock Data Retrieval**: For each unique ticker involved in the transactions, historical stock price data was fetched from Yahoo Finance using the `get_data` function. The data spanned from the date of the earliest transaction to the present.

3. **Daily Returns Calculation**: Daily returns for each stock were computed based on the adjusted close prices. The formula used was:

$$
\text{Daily Return} = \frac{\text{Price}_{t} - \text{Price}_{t-1}}{\text{Price}_{t-1}}
$$

4. **Portfolio Valuation**: A portfolio dataframe was constructed with columns representing each stock, cash holdings, and total portfolio value. Each row represented a day from the start date of the earliest transaction to the present.

5. **Transaction Effect on Portfolio**: Transactions were applied sequentially, updating stock holdings and cash balances appropriately. Purchases decreased cash holdings and increased stock positions, while sales did the reverse.

6. **Daily and Cumulative Returns Calculation**: The daily return was calculated using Time Weight Return with the following formula:

$$
\text{Daily Return} = \frac{\text{Total Value}_{t} - \text{Total Value}_{t-1} - \text{Cash Flow}_{t}}{\text{Total Value}_{t-1} + \text{Cash Flow}_{t}}
$$

Cumulative returns were then computed as the running product of (1 + daily return), subtracting 1 to reflect the overall return relative to the initial value.


### Marking Insider Trades

`mark_insider.ipynb`: To flag trades as insider and create the final `insider_returns.csv`, firstly Committee data from both the 
House and Senate were merged, and duplicate entries were removed to streamline the dataset. A name matching algorithm was employed 
to align names between the congressional and transaction datasets. This step was crucial for accurately linking stock transactions 
to specific lawmakers. The processed committee data was merged with transaction data based on matched names, enabling us to correlate 
stock trades with committee memberships. For each transaction linked to a congressman, we checked whether the traded stock belonged to 
an industry sector overseen by a committee on which the congressman serves. This was facilitated by the committee-sector mapping. The 
resulting dataset is saved as `insider_marked_trades.csv`.

## Results

The hypothesis that Congressional insider trading consistently outperforms the S&P 500 is only partially supported. 
While the average Congressional and Insider Flagged returns do not consistently outperform the market, significant 
outperformance is observed in the top echelons of Congress, particularly among the Top 50 and more markedly in the 
Top 10 insiders. These findings indicate that while the broader Congress does not generally outperform the market, 
a select group within Congress possibly utilizes their position or insider information to achieve superior trading 
outcomes. This report suggests a need for further investigation and possibly stricter regulations to ensure fairness 
and transparency in Congressional trading activities. Our member lookup features gives a clear indication of who and 
by how much.

[^1]: [Pew Research Center](https://www.pewresearch.org/politics/2023/09/19/public-trust-in-government-1958-2023/)
[^2]: [Business Insider](https://www.businessinsider.com/poll-stock-trading-ban-congress-2022-6)
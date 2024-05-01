import streamlit as st

st.set_page_config(
    page_title="Appendix",
    page_icon="📑",
)

st.write("# Project Purpose and Appendix")

st.write(
'''
## Introduction/Motivation
Public trust in officials has been eroding for quite some time now. According to the Pew Research Center, since 2000, public trust has fallen from 44% to 16%.
This 64% degradation can be attributed to many things, such as long wars in the middle east, China's rise, and divisive presidential election cycles.
A large part of this distrust however, comes from congressmen and women’s ability to trade stocks. In 2012, congress passed the STOCK act, forcing members of congress to disclose any trades they make.
However this bill leaves a lot to be desired. Members of congress don’t have to disclose their trades until 30 days after the fact and failure to do so results in a mere 200 dollar fine.
This bill has seemingly done nothing to stop congress from trading stocks. Back in 2022, Business insider polled likely voters, and found that 70% of them would like to see a ban on lawmakers playing the stock market.
We created this project in an attempt to shed some light on congressional trades, and to see if they are seeing significant returns above average, if their party has anything to do with whether or not they trade, and if the committee they sit on affects what industry they invest in.
## Hypotheses
1. Congressional insider trading will consistently outperform the S&P 500.
2. The disclosure of trading activities by members of certain committees exerts varied impacts on stock performance. Specifically, committees associated with finance, healthcare, and technology wield a pronounced influence on the stocks they trade, resulting in notable price fluctuations following the revelation of such activities.
## Data Collection
Issues we ran into:
Stocks going private/mergers & acquisitions
- Certain transactions were with private companies, which congresspeople still need to disclose. We have the data on these disclosures, but we don’t have the data on the pricing. We excluded these from our calculations and saved them in bad_tickers.txt. 
- Stocks that were delisted/taken private caused us issues as well. We were only able to calculate the returns up until the last day they were public. This caused discrepancies in the calculation of the estimated profit/loss of the investor’s portfolio. The actual return of their portfolio still goes on after it’s private. There was no way to combat this due to issues collecting the pricing data.
Web Scraping
- We scraped two government websites: https://www.house.gov/representatives and https://www.senate.gov/general/committee_assignments/assignments.htm. We also scraped wikipedia to get senators’ party and state, as this was not in the data on the government website.
Merging these datasets proved to be a challenge based on the difference in names both websites had, in which we did some manual fixes. We’ll run into this problem again down the line when processing data with returns.
Yahoo Finance
- We used yahoo finance to get the daily returns for individual stocks and the S&P 500 index.
## Data Processing
Merging
- Merging the transactions data with our congresspeople data was difficult, again, due to the differences in how the names were formatted. We had to change them for each congressperson after the fact.
- Adding gsector to the committee was a challenge, we had to brute force our way through. We did this by going to every committee’s websites and reading what they stand for and how they interact with the business world.
Their mission statements provided us with some insights, but reading their committee reports allowed us to see the bigger picture.
We also looked into online results for how the committee operates. These actions allowed us to pair a committee with the GICS sector they most likely oversee, and thus most likely to have insider information.
- To flag for insider trading, we used the merged dataset with the 
Calculations
- Calculating portfolio returns proved to be the greatest challenge. We tried multiple different methods, such as calculating a Time Weighted Return or a Dollar Weighted Return based on our estimates, each to no avail.
We decided on calculating the total portfolio value and finding percent change day-by-day, then cumulating.

Final Datasets
- Daily Cumulative Returns for the S&P 500
- Individual trades per congressperson
- Daily Cumulative Returns of all trades per congressperson
- Daily Cumulative Returns of insider trades per congressperson
## Results
We've found that our first hypothesis was not supported by the analysis. The portfolio of the 'average' congress member consistently underperforms the S&P 500. However, it does follow a very similar curve, indicitive of a well diversified portfolio. 
There are some specific congress members that do consistently outperform the market. The Member Lookup section of this dashboard ranks the members by their performance and can highlight some of the most profitable portfolios!

'''
)
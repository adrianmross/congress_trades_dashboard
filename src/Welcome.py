import streamlit as st

st.set_page_config(
    page_title="Congress Trades Dashboard",
    page_icon=" 🇺🇸",
)

st.write("# Welcome to the Sus' Congress Trades Project!")

st.write("##### Brought to you by: The Inside Indexers")

st.markdown("""
### Pages:
- **Congress v. Market** compares the S&P 500 to Congress members' average cumulative returns
- **Member Lookup** does the same thing, but you can isolate specific congress members and view all their trades
- **EDA** allows you to explore the data and see the impact of Congress members' disclosures on the industry
- **Appendix** is a report that explains our processes and analysis
""")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    ### GitHub Repository
    - [GitHub Repository](https://github.com/adrianmross/congress_trades_dashboard)

    #### Acknowledgements
    1. Unusual Whales is a group that came out with a viral report on Congress members' stock trades. They have been a source of inspiration for our project as well as a source for calculation methodologies.
    2. The New York Times article on Congress Stock Trades: [NYT Article: Stock Trades Reported by Nearly a Fifth of Congress Show Possible Conflicts](https://www.nytimes.com/interactive/2022/09/13/us/politics/congress-stock-trading-investigation.html) gave us the idea to analyze conflicts of interest in Congress.
    3.  Information on trades made by members of Congress is from the [House and Senate Stock Watcher API](https://senatestockwatcher.com/api) which is a free and real-time API that provides information on trades made by members of Congress based on their financial disclosures from the STOCK Act.
    """
)

# st.markdown(
#     """
#     Streamlit is an open-source app framework built specifically for
#     Machine Learning and Data Science projects.
#     **👈 Select a demo from the sidebar** to see some examples
#     of what Streamlit can do!
#     ### Want to learn more?
#     - Check out [streamlit.io](https://streamlit.io)
#     - Jump into our [documentation](https://docs.streamlit.io)
#     - Ask a question in our [community
#         forums](https://discuss.streamlit.io)
#     ### See more complex demos
#     - Use a neural net to [analyze the Udacity Self-driving Car Image
#         Dataset](https://github.com/streamlit/demo-self-driving)
#     - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
# """
# )

import streamlit as st

st.set_page_config(
    page_title="Congress Trades Dashboard",
    page_icon=" 🇺🇸",
)

st.write("# Welcome to the Sus' Congress Trades Project!")

st.write("##### Brought to you by: The Inside Indexers")

st.write("### Outline:")
st.write("Congress v. Market compares the S&P 500, an average congress member, and the top 50 congress member portfolios")
st.write("Member Lookup does the same thing, but you can isolate specific congress members")
st.write("EDA...")
st.write("Appendix is a report that explains our processes and some analysis")

st.sidebar.success("Select a page above.")

st.write("## Performance of U.S. Congressional Insider Trades Dashboard 🇺🇸")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

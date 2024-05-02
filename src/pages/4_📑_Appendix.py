import streamlit as st

st.set_page_config(
    page_title="Appendix",
    page_icon="📑",
)

with open('report.md', 'r') as f:
    report = f.read()

st.write(report)
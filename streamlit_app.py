import streamlit as st
from display import Presentation

# Set page title and layout
st.set_page_config(
    page_title="CPI Machines",
    layout="wide",
)

present = Presentation()

st.title("Consumer Price Index in the USA")
present.cpi()
present.notes()

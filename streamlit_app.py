import streamlit as st
from display import Presentation

# Set page title and layout
st.set_page_config(
    page_title="CPI Machine",
    layout="wide",
)

present = Presentation()

st.title("Inflation Expectations as Measured by the Consumer Price Index (CPI) in the USA")
present.cpi()
present.notes()

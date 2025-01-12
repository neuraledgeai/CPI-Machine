import streamlit as st
from display import Presentation

# Set page title and layout
st.set_page_config(
    page_title="CPI Machine",
    layout="wide",
)

present = Presentation()

st.title("Inflation Expectations in the USA as Measured by the Consumer Price Index (CPI)")

options = ["Headline Inflation", "Core Inflation"]
selection = st.segmented_control(
    " ", options, default="Headline Inflation"
)
if selection == "Headline Inflation":
    present.inflation()
else:
    present.coreInflation()

present.notes()

from business import Model
import streamlit as st
import plotly.express as px

class Presentation:
  
  def __init__(self):
    self.model = Model()

  def cpi(self):
    
    option = st.selectbox(
      "Units/Index:",
      (
        "Inflation",
        "Core Inflation",
        "Inflation (percent change)",
        "Core Inflation (percent change)"
      ),
    )
    df = self.model.predict(result="dataframe")
    # Filter for predicted values (2024–2033)
    df_predicted = df[df["Label"] == "Predicted"]
    
    # Calculate the mean CPI and CCPI for the predicted values
    mean_cpi = df_predicted["CPI"].mean()
    mean_ccpi = df_predicted["CCPI"].mean()
    
    # Get the actual CPI and CCPI values for 2023
    actual_cpi_2023 = df.loc["2023-01-01", "CPI"]
    actual_ccpi_2023 = df.loc["2023-01-01", "CCPI"]
    
    # Calculate percent change from 2023 actual to predicted mean
    percent_change_cpi = ((mean_cpi - actual_cpi_2023) / actual_cpi_2023) * 100
    percent_change_ccpi = ((mean_ccpi - actual_ccpi_2023) / actual_ccpi_2023) * 100

    # Calculate Purchasing Power for 2023 and 2033
    pp_cpi_2023 = 100 / df.loc["2023-01-01", "CPI"]
    pp_cpi_2033 = 100 / df.loc["2033-01-01", "CPI"]
    
    pp_ccpi_2023 = 100 / df.loc["2023-01-01", "CCPI"]
    pp_ccpi_2033 = 100 / df.loc["2033-01-01", "CCPI"]

    # Calculate Percent Change in Purchasing Power
    pp_cpi_change = ((pp_cpi_2033 - pp_cpi_2023) / pp_cpi_2023) * 100
    pp_ccpi_change = ((pp_ccpi_2033 - pp_ccpi_2023) / pp_ccpi_2023) * 100
    
    if option == "Inflation":
      result = "fig_cpi"
      cpi = mean_cpi.round(3)
      cpi_percent_change = percent_change_cpi.round(3)
      purchasing_power = pp_cpi_2033.round(3)
      purchasing_power_percent_change = pp_cpi_change.round(3)
    elif option == "Inflation (percent change)":
      result = "fig_cpi_pct_chg"
      cpi = mean_cpi.round(3)
      cpi_percent_change = percent_change_cpi.round(3)
      purchasing_power = pp_cpi_2033.round(3)
      purchasing_power_percent_change = pp_cpi_change.round(3)
    elif option == "Core Inflation":
      result = "fig_ccpi"
      cpi = mean_ccpi.round(3)
      cpi_percent_change = percent_change_ccpi.round(3)
      purchasing_power = pp_ccpi_2033.round(3)
      purchasing_power_percent_change = pp_ccpi_change.round(3)
    elif option == "Core Inflation (percent change)":
      result = "fig_ccpi_pct_chg"
      cpi = mean_ccpi.round(3)
      cpi_percent_change = percent_change_ccpi.round(3)
      purchasing_power = pp_ccpi_2033.round(3)
      purchasing_power_percent_change = pp_ccpi_change.round(3)
      
    fig = self.model.predict(result = result)
    
    # Improve the layout and design
    fig.update_layout(
        dragmode=False,
        title_font=dict(size=17, family="Arial"),
        xaxis=dict(
            showgrid=True, 
            gridcolor="lightgrey",
            rangeslider=dict(visible=True, bgcolor="#636EFA", thickness=0.05),  
        ),
        yaxis=dict(showgrid=True, gridcolor="lightgrey"),
    )
    
    st.plotly_chart(fig)
    
    col1, col2 = st.columns(2)
    col1.metric(
      "10 Year Avg. CPI (2023-33)",
      cpi,
      f"{cpi_percent_change}%",
      help =f"The average Consumer Price Index (CPI) over the 10 years from 2024 to 2033 is expected to represent a {cpi_percent_change}% increase compared to the CPI value in 2023.",
      border=True
    )
    col2.metric(
      "Purchasing Power (2033)",
      f"{purchasing_power * 100}%",
      f"{purchasing_power_percent_change}%",
      border=True,
      help =f"On average, the purchasing power of $1.00 in 2033 is expected to be only {purchasing_power * 100}% of its value during the base period (1982-1984). It is expected to represent a {purchasing_power_percent_change}% decrease compared to 2023."
    )

  def notes(self):
    st.info("Notes")
    content = """
    <div style="text-align: justify; font-size: 12px;">
        <p>The Consumer Price Index for All Urban Consumers: All Items (Inflation) is a price index of a basket of goods and services paid by urban consumers in the United States. 
        It is compiled by the U.S. Bureau of Labor Statistics and measures changes in the price level of this basket over time. The index is used to assess price changes associated 
        with the cost of living and is a key indicator of inflation. The data reflects the spending patterns of urban consumers, which represent approximately 93% of 
        the total U.S. population.</p>
        <p>The Consumer Price Index for All Urban Consumers: All Items Less Food and Energy (Core Inflation) is a price index that measures the changes in the cost of a basket of goods 
        and services, excluding the volatile food and energy sectors. This index is also compiled by the U.S. Bureau of Labor Statistics and is used to provide a clearer view of 
        the underlying inflation trends by excluding the often fluctuating prices of food and energy.</p>
        <p>The model used for predictions is trained on historical Consumer Price Index data from 1960 up to 2023. Therefore, the predictions generated by the model start from the year 2024 onwards. It 
        is important to note that the model may make mistakes, and individual predictions might not always be accurate. However, the reliability of the model's predictions can be 
        assessed based on their average accuracy over time.</p>
    </div>
    """
    
    st.markdown(content, unsafe_allow_html=True)

from business import Model
import streamlit as st
import plotly.express as px

class Presentation:
  
  def __init__(self):
    self.model = Model()

  def inflation(self):
    
    option = st.selectbox(
      "Units:",
      (
        "Consumer Price Index: All Items",
        "Percent Change"
      )
    )
    
    df = self.model.predict(result="dataframe")

    # Filter for predicted values (2024–2033)
    df_predicted = df[df["Label"] == "Predicted"]

    # Calculate the mean CPI and PP for the predicted values
    mean_cpi = df_predicted["CPI"].mean()
    mean_pp = df_predicted["PP"].mean()
    
    # Get the actual CPI and PP values for 2023
    actual_cpi_2023 = df.loc["2023-01-01", "CPI"]
    actual_pp_2023 = df.loc["2023-01-01", "PP"]
    
    
    # Calculate percent change in CPI from 2023 actual to predicted mean
    percent_change_cpi = ((mean_cpi - actual_cpi_2023) / actual_cpi_2023) * 100
    
    # Calculate percent change in PP from 2023 actual to predicted mean
    percent_change_pp = ((mean_pp - actual_pp_2023) / actual_pp_2023) * 100

    if option == "Consumer Price Index: All Items":
      result = "fig_cpi"
      heading_text = "Consumer Price Index for All Urban Consumers: All Items in U.S. City Average (1961-2033)"
    elif option == "Percent Change":
      result = "fig_cpi_pct_chg"
      heading_text = "Consumer Price Index for All Urban Consumers: All Items in U.S. City Average, Percent Change From Year Ago (1961-2033)"
      
    heading = f"""
    <div style="text-align: center; font-size: 18px;">
        <strong>{heading_text}</strong>
    </div>
    """  
    
    fig = self.model.predict(result = result)
    
    # Improve the layout and design
    fig.update_layout(
        dragmode=False,
        xaxis=dict(
            showgrid=True, 
            gridcolor="lightgrey",
            rangeslider=dict(visible=True, bgcolor="#636EFA", thickness=0.05),  
        ),
        yaxis=dict(showgrid=True, gridcolor="lightgrey"),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.markdown(heading, unsafe_allow_html=True)
    config = {
        'displayModeBar': False,  # Hide the mode bar
        'displaylogo': False,     # Hide the Plotly logo
        'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 
                                   'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']
    }
    
    st.plotly_chart(fig, config=config)
    
    col1, col2 = st.columns(2)
    col1.metric(
      "10 Year Avg. CPI: All Items (2024-33)",
      mean_cpi.round(2),
      f"{percent_change_cpi.round(2)}%",
      help =f"On average, the general price level in the USA is expected to increase by {percent_change_cpi.round(2)}% over the next 10 years, indicating a significant rise in inflation.",
      border=True
    )
    col2.metric(
      "10 Year Avg. Purchasing Power (2024-33)",
      f"{mean_pp.round(2) * 100}%",
      f"{percent_change_pp.round(2)}%",
      border=True,
      help =f"On average, the purchasing power of $1.00 over the next 10 years is expected to be only {mean_pp.round(2) * 100}% of its value during the base period (1982-1984). This represents a {percent_change_pp.round(2)}% decrease compared to its purchasing power in 2023."
    )
    
    # Display the key highlights.
    with st.expander("Key Highlights", expanded = True):
      st.markdown(f''':blue-background[Highlight-1] : On average, the general price level in the USA is expected to increase by {percent_change_cpi.round(2)}% over the next 10 years, indicating a significant rise in inflation.''')
      st.markdown(f''':blue-background[Highlight-2] : On average, the purchasing power of $1.00 over the next 10 years is expected to be only {mean_pp.round(2) * 100}% of its value during the base period (1982-1984). This represents a {percent_change_pp.round(2)}% decrease compared to its purchasing power in 2023.''')

  def coreInflation(self):
    
    option = st.selectbox(
      "Units:",
      (
        "Consumer Price Index: All Items Less Food and Energy",
        "Percent Change"
      )
    )

    df = self.model.predict(result="dataframe")
    
    # Filter for predicted values (2024–2033)
    df_predicted = df[df["Label"] == "Predicted"]
    
    # Calculate the mean CCPI and CPP for the predicted values
    mean_ccpi = df_predicted["CCPI"].mean()
    mean_cpp = df_predicted["CPP"].mean()
    
    # Get the actual CCPI and CPP values for 2023
    actual_ccpi_2023 = df.loc["2023-01-01", "CCPI"]
    actual_cpp_2023 = df.loc["2023-01-01", "CPP"]
    
    # Calculate percent change in CCPI from 2023 actual to predicted mean
    percent_change_ccpi = ((mean_ccpi - actual_ccpi_2023) / actual_ccpi_2023) * 100
    
    # Calculate percent change in CPP from 2023 actual to predicted mean
    percent_change_cpp = ((mean_cpp - actual_cpp_2023) / actual_cpp_2023) * 100
    
    
    if option == "Consumer Price Index: All Items Less Food and Energy":
      result = "fig_ccpi"
      heading_text = "Consumer Price Index for All Urban Consumers: All Items Less Food and Energy in U.S. City Average (1961-2033)"
    elif option == "Percent Change":
      result = "fig_ccpi_pct_chg"
      heading_text = "Consumer Price Index for All Urban Consumers: All Items Less Food and Energy in U.S. City Average, Percent Change From Year Ago (1961-2033)"
  
    heading = f"""
    <div style="text-align: center; font-size: 18px;">
        <strong>{heading_text}</strong>
    </div>
    """  
    
    fig = self.model.predict(result = result)
    
    # Improve the layout and design
    fig.update_layout(
        dragmode=False,
        xaxis=dict(
            showgrid=True, 
            gridcolor="lightgrey",
            rangeslider=dict(visible=True, bgcolor="#636EFA", thickness=0.05),  
        ),
        yaxis=dict(showgrid=True, gridcolor="lightgrey"),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.markdown(heading, unsafe_allow_html=True)
    config = {
        'displayModeBar': False,  # Hide the mode bar
        'displaylogo': False,     # Hide the Plotly logo
        'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 
                                   'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']
    }
    st.plotly_chart(fig, config=config)
    
    col1, col2 = st.columns(2)
    col1.metric(
      "10 Year Avg. CPI: All Items Less Food and Energy (2024-33)",
      mean_ccpi.round(2),
      f"{percent_change_ccpi.round(2)}%",
      help =f"On average, the core price level in the USA is expected to increase by {percent_change_ccpi.round(2)}% over the next 10 years, indicating a significant rise in core inflation.",
      border=True
    )
    col2.metric(
      "10 Year Avg. Purchasing Power (2024-33)",
      f"{mean_cpp.round(2) * 100}%",
      f"{percent_change_cpp.round(2)}%",
      border=True,
      help =f"On average, the purchasing power of $1.00 over the next 10 years is expected to be only {mean_cpp.round(2) * 100}% of its value during the base period (1982-1984). This represents a {percent_change_cpp.round(2)}% decrease compared to its purchasing power in 2023."
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

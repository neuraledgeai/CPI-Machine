import joblib
import pandas as pd
from database import LocalDatabase 
import plotly.express as px


class Model:
  def __init__(self, cpi_model="cpi_model.pkl", m2_model="m2_model.pkl", ccpi_model="ccpi_model.pkl"):
    self.cpi_model = joblib.load("cpi_model.pkl")
    self.m2_model = joblib.load("m2_model.pkl")
    self.ccpi_model = joblib.load("ccpi_model.pkl")
    self.db = LocalDatabase()

  def predict(self, years = range(1,11), result="fig_cpi"):
    # Load training data from database
    df = self.db.load_data()
    
    # Initialize M2 value and corresponding year
    m2 = 20810.3  # M2 for 2023
    corresponding_year = 2023
    
    # Lists to store predicted M2s and corresponding years
    predicted_m2s = []
    corresponding_years = []
    
    for year in years:
        # Prepare the data for prediction
        #X = np.array([[m2]])
        X = pd.DataFrame({"M2_L1": [m2]})
    
        # Make prediction using the trained model
        predicted_m2 = self.m2_model.predict(X)
    
        # Update M2 and corresponding year for the next iteration
        m2 = predicted_m2[0]  # Update the value of m2 for the next year
        corresponding_year += 1
    
        # Append the results to the respective lists
        predicted_m2s.append(predicted_m2[0])  # Store as a scalar
        corresponding_years.append(corresponding_year)

    # Create a DataFrame to store forecasted results
    df_predicted_m2 = pd.DataFrame({
      "Year": corresponding_years,
      "M2": predicted_m2s
    })
    
    # Convert Year to pandas datetime and set as index
    df_predicted_m2["Year"] = pd.to_datetime(df_predicted_m2["Year"], format="%Y")
    df_predicted_m2.set_index("Year", inplace=True)
    
    # Predict CPI
    predicted_cpis = self.cpi_model.predict(df_predicted_m2)  

    # Predict CCPI
    predicted_ccpis = self.ccpi_model.predict(df_predicted_m2)  
    
    # Create a DataFrame with the predicted CPI values and the corresponding datetime index
    df_predicted_cpi = pd.DataFrame(
        predicted_cpis, 
        columns=["CPI"],  # Name of the column with predictions
        index=df_predicted_m2.index  # Use the same datetime index from df_predicted_m2
    )

    # Create a DataFrame with the predicted CCPI values and the corresponding datetime index
    df_predicted_ccpi = pd.DataFrame(
        predicted_ccpis, 
        columns=["CCPI"],  # Name of the column with predictions
        index=df_predicted_m2.index  # Use the same datetime index from df_predicted_m2
    )
    
    # Drop `M2` from `df`
    df = df.drop(columns=["M2"])
    
    #  Concatenate predicted CPI and CCPI dataframes horizontally
    df_predicted_cpis = pd.concat([df_predicted_cpi, df_predicted_ccpi], axis=1)

    #Align the index of df_predicted_cpis with df_predicted_m2
    df_predicted_cpis.index = df_predicted_m2.index

    # Concatenate the original dataframe with the predicted values
    df = pd.concat([df, df_predicted_cpis])

    # Calculate Percent Change Year Ago for CPI and CCPI
    df["CPI_PC"] = df["CPI"].pct_change() * 100
    df["CCPI_PC"] = df["CCPI"].pct_change() * 100
    
    # Drop rows with NaN values resulting from percent change calculation
    df = df.dropna()

    # Add a 'Label' column
    df["Label"] = ["Actual" if idx.year <= 2023 else "Predicted" for idx in df.index]

    # Figure for CPI
    fig_cpi = px.line(
        df,
        x=df.index,
        y="CPI",
        title=(" "),
        labels={
            "CPI": "CPI (Index 1982-1984=100)",
            "index": "Year"
        },
        template="plotly_white"
    )

    # Figure for CCPI
    fig_ccpi = px.line(
        df,
        x=df.index,
        y="CCPI",
        title=(" "),
        labels={
            "CCPI": "CPI (Index 1982-1984=100)",
            "index": "Year"
        },
        template="plotly_white"
    )

    # Figure for CPI percent change
    fig_cpi_pc = px.line(
        df,
        x=df.index,
        y="CPI_PC",
        title=(" "),
        labels={"CPI_PC": "CPI % Change a Year Ago", "index": "Year"},
        template="plotly_white"
    )

    # Figure for CCPI percent change
    fig_ccpi_pc = px.line(
        df,
        x=df.index,
        y="CCPI_PC",
        title=(" "),
        labels={"CCPI_PC": "CPI % Change a Year Ago", "index": "Year"},
        template="plotly_white"
    )

    if result == "fig_cpi":
        fig = fig_cpi
    elif result == "fig_cpi_pct_chg":
        fig = fig_cpi_pc
    elif result == "fig_ccpi":
        fig = fig_ccpi
    elif result == "fig_ccpi_pct_chg":
        fig = fig_ccpi_pc
    elif result == "dataframe":
        fig = df
    
    return fig

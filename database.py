import pandas as pd

class LocalDatabase:
  def __init__(self, cpi_dataset="CPI_for_urban_consumers_all_items_US_city_average.csv", m2_dataset="M2.csv", ccpi_dataset="CPILFESL.csv"):
    self.cpi = pd.read_csv(cpi_dataset)  
    self.m2 = pd.read_csv(m2_dataset)
    self.ccpi = pd.read_csv(ccpi_dataset)
    self.df = None  # Placeholder for the processed DataFrame

  def load_data(self):
    # If the DataFrame is already processed, return it directly
    if self.df is not None:
        return self.df
      
    # Convert 'observation_date 'to datetime and assign to 'Date'
    self.cpi["Date"] = pd.to_datetime(self.cpi["observation_date"]) 
    self.m2["Date"] = pd.to_datetime(self.m2["observation_date"])
    self.ccpi["Date"] = pd.to_datetime(self.ccpi["observation_date"])

    # Drop the 'observation_date' column
    self.cpi.drop(columns=["observation_date"], inplace=True)
    self.m2.drop(columns=["observation_date"], inplace=True)
    self.ccpi.drop(columns=["observation_date"], inplace=True)

    # Rename columns
    self.cpi.rename(columns={"CPIAUCSL": "CPI"}, inplace=True)
    self.m2.rename(columns={"M2SL": "M2"}, inplace=True)
    self.ccpi.rename(columns={"CPILFESL": "CCPI"}, inplace=True)
    
    # Set 'Date' as the index for both dataframes
    self.cpi.set_index("Date", inplace=True)
    self.m2.set_index("Date", inplace=True)
    self.ccpi.set_index("Date", inplace=True)
    
    # Concatenate the two DataFrames along the columns
    self.df = pd.concat([self.cpi, self.m2, self.ccpi], axis=1)

    return self.df

    

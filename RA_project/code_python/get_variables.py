"""
Purpose : get interest rate, SP500, unemployement after each reunion in order to expand our database
"""


"""
Get Dates
"""

import pandas as pd

df_interest_rate = pd.read_csv("/Users/etiennelenaour/Desktop/Stage/csv_files/fed-funds-rate-historical-chart.csv")

print(df_interest_rate.head())


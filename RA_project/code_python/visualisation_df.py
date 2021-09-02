import pandas as pd 


df = pd.read_csv('/Users/etiennelenaour/Desktop/Stage/csv_files/final_df_v1.csv')

print(df.iloc[80272:80292,2:7])
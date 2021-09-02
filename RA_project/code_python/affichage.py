import pandas as pd
import datetime
import matplotlib.pyplot as plt



project_directory = '/Users/etiennelenaour/Desktop/Stage/'

df_incert = pd.read_csv(project_directory + "csv_files/" + "df_traitement_finale_incertitude.csv")

print(len(df_incert.Name.unique()))
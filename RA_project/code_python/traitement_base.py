import pandas as pd
import numpy as np



project_directory = '/Users/etiennelenaour/Desktop/Stage/'


df_statement_by_lines = pd.read_csv(project_directory + "csv_files/" + "df_statement_real.csv")


"""
pb du vice chairman
"""

for ii in range(len(df_statement_by_lines.interlocutor_name)):

	nom = df_statement_by_lines.interlocutor_name[ii] 
	if "VICE" in nom.split(" "):
		liste_statement = df_statement_by_lines.statement[ii].split(" ")
		good_liste = liste_statement[1:]
		df_statement_by_lines.statement[ii] = " ".join(good_liste)

	else:
		pass


for ii in range(len(df_statement_by_lines.interlocutor_name)):
	if type(df_statement_by_lines["statement"][ii]) == str:
		df_statement_by_lines["statement"][ii] = df_statement_by_lines["statement"][ii].lower()
	else:
		pass


df_statement_by_lines.to_csv(project_directory + "csv_files/" + "final_dataframe.csv")

"""
pb du lower case
"""
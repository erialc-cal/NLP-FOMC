import pandas as pd
import datetime
import matplotlib.pyplot as plt


project_directory = '/Users/etiennelenaour/Desktop/Stage/'


df_affirmation = pd.read_csv(project_directory + "csv_files/" + "df_affirmation_finale.csv")
df_score = pd.read_csv(project_directory + "csv_files/" + "df_score_posi_finale.csv")

df_incertitude = pd.read_csv(project_directory + "csv_files/" + "df_score_incertitude_finale.csv")


def creation_colonne_tx_i(true_df, df_with_info):

	liste_tx_i = list()

	for date in true_df["Date"]:
		liste_tx_i.append(list(df_with_info[df_with_info["Date"] == date]["nasdaq_value"])[0])


	return liste_tx_i



liste_tx_i = creation_colonne_tx_i(df_score, df_affirmation)

df_score["nasdaq_value"] = liste_tx_i


liste_tx_i_second = creation_colonne_tx_i(df_incertitude, df_affirmation)
df_incertitude["nasdaq_value"] = liste_tx_i_second

df_score_greenspan = df_score[df_score["Chair"] == "CHAIRMAN GREENSPAN."]
df_score_bernanke  = df_score[df_score["Chair"] == "CHAIRMAN BERNANKE."]


df_incertitude_greenspan = df_incertitude[df_incertitude["Chair"] == "CHAIRMAN GREENSPAN."]
df_incertitude_bernanke  = df_incertitude[df_incertitude["Chair"] == "CHAIRMAN BERNANKE."]


def create_df_comuns_Name(df_green, df_ber):

	list_intersect = list(set(df_green["Name"]).intersection(set(df_ber["Name"])))
	liste_df = list()
	big_df = pd.concat([df_green, df_ber], axis=0)
	
	df_intersect = big_df[big_df['Name'].isin(list_intersect)]


	s = df_intersect['Name'].value_counts() > 10
	print(df_intersect['Name'].value_counts())
	liste_index = s[s].index

	df_finale = df_intersect[df_intersect['Name'].isin(liste_index)]
	df_finale = df_finale[df_finale['Name'] != 'MR. BERNANKE.']


	return df_finale



df_finale = create_df_comuns_Name(df_score_greenspan, df_score_bernanke)
df_finale.to_csv(project_directory + "csv_files/" + "df_traitement_finale_posi.csv")



df_finale_second = create_df_comuns_Name(df_incertitude_greenspan, df_incertitude_bernanke)
df_finale_second.to_csv(project_directory + "csv_files/" + "df_traitement_finale_incertitude.csv")











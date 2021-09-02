import pandas as pd 
import numpy as np 



project_directory = '/Users/etiennelenaour/Desktop/Stage/'



df = pd.read_csv(project_directory + "csv_files/" + "final_df_v1.csv")

#print(df.columns)


liste_nb_mot_per_reunion = list()
liste_nb_mot_chair = list()
liste_date = list()
liste_chair_in_charge = list()


liste_nb_mot_per_reunion = df.groupby("Date").sum()["statement _size"].values
liste_date = df.Date.unique()

for date in liste_date:
	df_date = df[df["Date"] == date]
	liste_chair_in_charge.append(df_date.chair_in_charge.unique()[0])



for date in liste_date:
	df_date = df[df["Date"] == date] 
	chair_in_charge = df_date.chair_in_charge.unique()[0]
	df_date_chair = df_date[df_date.interlocutor_name == chair_in_charge]
	liste_nb_mot_chair.append(df_date_chair["statement _size"].sum())


liste_ratio_chair = list()

for ii in range(len(liste_nb_mot_chair)):
	liste_ratio_chair.append(liste_nb_mot_chair[ii] / liste_nb_mot_per_reunion[ii])



df_finale = pd.DataFrame(list(zip(liste_date, liste_nb_mot_per_reunion, liste_nb_mot_chair, liste_ratio_chair, liste_chair_in_charge)), 
               columns =['Date', 'Nb_word_per_meeting', 'Nb_word_chair', 'Ratio_chair', 'chair_in_charge']) 


df_finale.to_csv(project_directory + "csv_files/" + "df_nb_word_per_meeting.csv")





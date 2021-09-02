import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import numpy as np


project_directory = '/Users/etiennelenaour/Desktop/Stage/'

df = pd.read_excel('/Users/etiennelenaour/Desktop/Stage/csv_files/df_statement_size.xlsx')


liste_date = list(df.Date.unique())

def create_liste_chair(df):

	liste_chair = list()
	chair_name = ['CHAIRMAN BURNS.', 'CHAIRMAN MILLER.', 'CHAIRMAN VOLCKER.', 'CHAIRMAN GREENSPAN.', 'CHAIRMAN BERNANKE.', 'CHAIR YELLEN.']

	for ele in df.interlocutor_name:

		if ele in chair_name:
			liste_chair.append(ele)

		else:
			liste_chair.append('Autre')


	return liste_chair


def idx_phrase(df):

	liste_idx = list()

	for ele in df.statement_number:
		numeric_carac = ''
		for carac in ele:
			if carac.isnumeric():
				numeric_carac += carac
			else:
				pass

		liste_idx.append(int(numeric_carac))

	return 	liste_idx



df['interlocuteur'] = create_liste_chair(df)
df['statement_nb'] = idx_phrase(df)




def found_chair_in_charge(df):

	chair_name = ['CHAIRMAN BURNS.', 'CHAIRMAN MILLER.', 'CHAIRMAN VOLCKER.', 'CHAIRMAN GREENSPAN.', 'CHAIRMAN BERNANKE.', 'CHAIR YELLEN.']
	chair_in_charge = list()
	liste_date = list(df.Date.unique())

	for date in liste_date:

		df_date = df[df.Date == date]

		for chair in chair_name:

			if chair in list(df_date.interlocuteur.unique()):
				le_bon = chair

			else:
				pass


		for ii in range(len(df_date.interlocuteur)):

			if le_bon != None:
				chair_in_charge.append(le_bon)

			else:
				chair_in_charge.append('autre')


	return chair_in_charge






def plot_reunion(df, date):

	ax = sns.barplot(x='statement_nb', y='statement _size', hue='interlocuteur', data=df, ci=None, palette=["red", "gray"])
	for i, t in enumerate(ax.get_xticklabels()):
		if (i % 50) != 0:
			t.set_visible(False)

	plt.xticks(rotation=90)
	ax.set(xlabel="Numéro de l'intervention", ylabel="Taille de l'intervention")
	date_real = str(date)[:10]
	plt.title("Temporalité de la réunion du :" + date_real)
	plt.savefig(project_directory + 'image_tempo/' + 'chair_tempo_' + date_real + '.png')
	plt.close()



def found_max(chair_in_charge, df):

	liste_nb_mot_moyen = list()
	liste_moment = list()

	df_chair = df[df.chair_in_charge == chair_in_charge]
	liste_date = list(df_chair.Date.unique())

	for date in liste_date:

		df_date = df_chair[df_chair.Date == date]

		df_date_and_chair = df_date[df_date.interlocuteur == chair_in_charge]

		statement_size_df = df_date_and_chair[['statement _size', 'statement_nb']]
		statement_size_df.set_index('statement_nb')
		

		best = statement_size_df['statement _size'].nlargest(3)

		size = len(df_date.interlocuteur)

		if best.index[0] > int(size * 0.6):
			indice = best.index[0]
			moment = statement_size_df['statement_nb'][indice]

		elif best.index[1] > int(size * 0.6):
			indice = best.index[1]
			moment = statement_size_df['statement_nb'][indice]

		elif best.index[2] > int(size * 0.6):
			indice = best.index[2]
			moment = statement_size_df['statement_nb'][indice]

		else :
			indice = statement_size_df['statement _size'].argmax()
			moment = statement_size_df['statement_nb'][indice]


		liste_moment.append(moment/size)

		total = df_date['statement _size'].sum()

		df_short = df_date[df_date.statement_nb > moment]
		df_short_short = df_short[df_short.interlocuteur != chair_in_charge]
		somme = df_short_short['statement _size'].sum()


		

		liste_nb_mot_moyen.append(somme/total)
		


	return liste_nb_mot_moyen, liste_moment





"""
MAIN
"""


liste_chair_in_charge = found_chair_in_charge(df)
df['chair_in_charge'] = liste_chair_in_charge




for date in liste_date:

	df_inter = df[df.Date == date]
	plot_reunion(df_inter, date)















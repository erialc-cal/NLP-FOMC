import pandas as pd 
import numpy as np 



project_directory = '/Users/etiennelenaour/Desktop/Stage/'

sentiment_score = pd.read_excel(project_directory + "csv_files/" +'inquirerbasic.xls')
df_true = pd.read_csv(project_directory + 'csv_files/final_df_v3.csv')



def creation_list(df, cate):

	final_list = list()

	for ii in range(len(df[cate])):

		if  df[cate][ii] == cate:
			final_list.append(df.Entry[ii])

		else:
			pass


	return final_list


def clean_list(liste):

	clean_list = list()

	for word in liste:

		if type(word) == str:

			good_word = list()


			for carac in word:
				if carac not in ["#", "-"] and not carac.isnumeric():
					good_word.append(carac)

				else:
					pass

			good_word_string = "".join(good_word)
			clean_list.append(good_word_string.lower())

		else:
			pass

	return clean_list


def compute_score(sentence, liste_score):

	score = 0
	total_score = 0

	for ele in sentence.split(" "):

		total_score += 1

		if ele in liste_score:
			score += 1

		else:
			pass

	if score > 0:
		final_score = score / total_score
	else:
		final_score = 0

	return final_score

###########################
#Création des listes#######
###########################


cate = ['Affil', 'Hostile', 'Strong', 'Power', 'Weak', 'Submit', 'Active', 'Passive', 'Ovrst', 'Undrst', 'Quan', 'ORD', 'CARD', 'NUMB', 'Yes', 'No', \
'Negate', 'SureLw', 'If', 'NotLw', 'RspGain', 'ABS', 'Causal']


liste_cate = [clean_list(creation_list(df=sentiment_score, cate=ele)) for ele in cate]


#Creation d'un df pour présenter ces scores



########################################
#Calcul des scores pour notre df #######
########################################


liste_score = [[] for i in range(len(cate))]


for sentence in df_true.statement:

	if type(sentence) == str:

		for idx, score in enumerate(liste_score):
			score.append(compute_score(sentence, liste_cate[idx]))


	else:
		for score in liste_score:
			score.append(0)



for idx, c in enumerate(cate):
	df_true[c] = liste_score[idx]



df_true.to_csv(project_directory + 'csv_files/final_df_v4.csv')















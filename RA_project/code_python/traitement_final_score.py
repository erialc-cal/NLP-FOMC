import pandas as pd 
import numpy as np 


###########################
#Chargement des données####
###########################

project_directory = '/Users/etiennelenaour/Desktop/Stage/'

sentiment_score = pd.read_excel(project_directory + "csv_files/" +'inquirerbasic.xls')
final_df = pd.read_csv(project_directory + "csv_files/" + "final_dataframe.csv")


###########################
#Création des fonctions####
###########################



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


liste_acadam = clean_list(creation_list(df=sentiment_score, cate='Academ'))
liste_Hostile = clean_list(creation_list(df=sentiment_score, cate='Hostile'))
liste_econo = clean_list(creation_list(df=sentiment_score, cate='Econ@'))
liste_Virtue = clean_list(creation_list(df=sentiment_score, cate='Virtue'))
liste_Vice = clean_list(creation_list(df=sentiment_score, cate='Vice'))


#Creation d'un df pour présenter ces scores



########################################
#Calcul des scores pour notre df #######
########################################


score_acadam, score_Hostile, score_econo, score_Virtue, score_Vice = list(), list(), list(), list(), list()


for sentence in final_df.statement:

	if type(sentence) == str:

		score_acadam.append(compute_score(sentence, liste_acadam)) 
		score_Hostile.append(compute_score(sentence, liste_Hostile))
		score_econo.append(compute_score(sentence, liste_econo))
		score_Virtue.append(compute_score(sentence, liste_Virtue))
		score_Vice.append(compute_score(sentence, liste_Vice))

	else:
		score_acadam.append(0) 
		score_Hostile.append(0)
		score_econo.append(0)
		score_Virtue.append(0)
		score_Vice.append(0)



final_df["score_acadam"] = score_acadam
final_df["score_hostile"] = score_Hostile
final_df["score_econo"] = score_econo
final_df["score_virtue"] = score_Virtue
final_df["score_vice"] = score_Vice



final_df.drop(['Unnamed: 0'], axis=1).to_csv(project_directory + "csv_files/" +"final_df_v1.csv")







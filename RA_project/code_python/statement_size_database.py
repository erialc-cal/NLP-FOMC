########
#Import#
########

import pandas as pd
import numpy as np



project_directory = '/Users/etiennelenaour/Desktop/Stage/'



df_sentiment = pd.read_excel('/Users/etiennelenaour/Desktop/Stage/vocab_sentiment.xlsx')
df_statement_by_lines = pd.read_csv(project_directory + "csv_files/" + "df_statement_real.csv")



"""
Liste de voca
"""

def remove_nan_from_list(liste):

	new_liste = list()

	for ele in liste:
		if type(ele) == str:
			new_liste.append(ele)
		else:
			pass

	return new_liste


negative_word_list = [ele.lower() for ele in df_sentiment.Negative.tolist()]
positive_word_list = [ele.lower() for ele in remove_nan_from_list(df_sentiment.Positive.tolist())]
strong_word_list = [ele.lower() for ele in remove_nan_from_list(df_sentiment.StrongModal.tolist())]
uncertainly_word_list = [ele.lower() for ele in remove_nan_from_list(df_sentiment.Uncertainly.tolist())]
weak_word_list = [ele.lower() for ele in remove_nan_from_list(df_sentiment.WeakModal.tolist())]


"""
Fonctions de calculs
"""

def compute_positivity_indiv(sentence):

    neg_score = 0
    pos_score = 0

    
    for ele in sentence.split(" "):

        if ele in negative_word_list:
            neg_score += 1

        elif ele in positive_word_list:
            pos_score += 1


        else:
             pass

    if pos_score > 0 or neg_score > 0:
    	score = (pos_score - neg_score) / (pos_score + neg_score)
    else:
    	score = 0

    return score


def compute_affirmation_indiv(sentence):

    strong_score = 0
    weak_score = 0

    for ele in sentence.split(" "):

        if ele in strong_word_list:
            strong_score += 1

        elif ele in weak_word_list:
            weak_score += 1

        else:
            pass

    if strong_score > 0 or weak_score > 0:
        score = (strong_score - weak_score) / (strong_score + weak_score)

    else:
        score = 0

    return score


def compute_uncertainly_indiv(sentence):

	uncertainly_score = 0
	total_score = 0

	for ele in sentence.split(" "):

		total_score += 1

		if ele in uncertainly_word_list:
			uncertainly_score += 1

		else:
			pass

	if uncertainly_score > 0:
		score = uncertainly_score / total_score
	else:
		score = 0

	return - score

"""
Appliquons cela à notre base de données
"""

liste_posi, liste_affi, liste_uncert = list(), list(), list()


for sentence in df_statement_by_lines.statement:

	if type(sentence) == str:

		liste_posi.append(compute_positivity_indiv(sentence))
		liste_uncert.append(compute_uncertainly_indiv(sentence))
		liste_affi.append(compute_affirmation_indiv(sentence))

	else:
		liste_posi.append(0)
		liste_uncert.append(0)
		liste_affi.append(0)



df_statement_by_lines["score_posi"] = liste_posi
df_statement_by_lines["score_affi"] = liste_affi
df_statement_by_lines["score_incert"] = liste_uncert


df_statement_by_lines.to_csv(project_directory + "csv_files/" + "df_statement_by_lines.csv")







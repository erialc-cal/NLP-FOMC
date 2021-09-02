import pandas as pd 
import numpy as np 



project_directory = '/Users/etiennelenaour/Desktop/Stage/'

df_sentiment = pd.read_excel('/Users/etiennelenaour/Desktop/Stage/vocab_sentiment.xlsx')
df_true = pd.read_csv(project_directory + 'csv_files/final_df_v3.csv')





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





def compute_positivity(statement):

	if type(statement) == str:

		liste_statement = statement.split(" ")

		neg_score = 0
		pos_score = 0

		

		for ele in liste_statement:

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

	else:
		score = 0

	return score


def compute_affirmation(statement):

	if type(statement) == str:

		liste_statement = statement.split(" ")

		strong_score = 0
		weak_score = 0

		for ele in liste_statement:


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
	else:
		score = 0

	return score


def compute_uncertainly(statement):

	if type(statement) == str:

		liste_statement = statement.split(" ")

		uncertainly_score = 0
		total_score = 0

		for ele in liste_statement:

			total_score += 1

			if ele in uncertainly_word_list:
				uncertainly_score += 1


			else:
				pass

		score = uncertainly_score / total_score

	else:
		score = 0

	return - score




liste_posi = list()
liste_affi = list()
liste_uncert = list()

for statement in df_true.statement:
	liste_posi.append(compute_positivity(statement))
	liste_affi.append(compute_affirmation(statement))
	liste_uncert.append(compute_uncertainly(statement))


df_true["score_posi"] = liste_posi
df_true["score_affi"] = liste_affi
df_true["score_uncert"] = liste_uncert

df_true.to_csv(project_directory + "csv_files/final_df_v3.csv")




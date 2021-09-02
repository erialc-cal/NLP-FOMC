import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import numpy as np
from scipy.stats import pearsonr

project_directory = '/Users/etiennelenaour/Desktop/Stage/'

df_sentiment = pd.read_excel('/Users/etiennelenaour/Desktop/Stage/vocab_sentiment.xlsx')
df = pd.read_csv(project_directory + "csv_files/" + "final_df_v1.csv")


"""
Fonctions
"""


def compute_hawkish_score(liste_statement):

	
	nb_dovish_word = 0
	nb_hawkish_word = 0

	liste_goal_voca =  ["inflation", "cyclical", "growth", "price", "wages", "development", "prices"]
	list_dovish_voca = ["decrease", "slow", "weak", "low", "decreased", "decreases", "decline", "slows"]
	list_hawkish_voca = ["increase", "fast", "strong", "high", "increased", "increases", "pressures", "pressure", "more"]

	for idx, word in enumerate(liste_statement):

		if word in liste_goal_voca:

			for subword in liste_statement[int(idx-2): int(idx+2)]:

				if subword in list_dovish_voca:
					nb_dovish_word += 1

				elif subword in list_hawkish_voca:
					nb_hawkish_word += 1

				else:
					pass
		
		else:
			pass

		if nb_hawkish_word > 0 or nb_dovish_word > 0:
			score = (nb_hawkish_word - nb_dovish_word) / (nb_hawkish_word + nb_dovish_word)
		else:
			score = 0

	return score

def remove_nan_from_list(liste):

	new_liste = list()

	for ele in liste:
		if type(ele) == str:
			new_liste.append(ele)
		else:
			pass

	return new_liste


"""
Score functions
"""     

negative_word_list = [ele.lower() for ele in df_sentiment.Negative.tolist()]
positive_word_list = [ele.lower() for ele in remove_nan_from_list(df_sentiment.Positive.tolist())]
strong_word_list = [ele.lower() for ele in remove_nan_from_list(df_sentiment.StrongModal.tolist())]
uncertainly_word_list = [ele.lower() for ele in remove_nan_from_list(df_sentiment.Uncertainly.tolist())]
weak_word_list = [ele.lower() for ele in remove_nan_from_list(df_sentiment.WeakModal.tolist())]



def compute_positivity(liste_statement):

	neg_score = 0
	pos_score = 0

	for ele in liste_statement:



		if ele in negative_word_list:
			neg_score += 1

		elif ele in positive_word_list:
			pos_score += 1


		else:
			pass

	if pos_score > 0 or neg_score > 0 :
		score = (pos_score - neg_score) / (pos_score + neg_score)

	else:
		score = 0

	return score

######################################################################################

def plot_score_hawkish(df):

    sns.relplot(x='Date', y='Score_Hawkish', hue='Chair', data=df)
    plt.xticks(rotation=90)
    plt.ylabel("Difference Hawkish Score")
    plt.title("Difference Hawkish Score by meeting (chair score - total score)")
    plt.show()
    plt.close()

######################################################################################

def plot_score_positivity_chair(df):

    sns.relplot(x='Date', y='Score_Pos', hue='Chair', data=df)
    plt.xticks(rotation=90)
    plt.ylabel("Positivity Chair")
    plt.title("Positivity Chair by meeting")
    plt.show()
    plt.close()


def plot_score_positivity_total(df):

    sns.relplot(x='Date', y='Score_Pos', hue='Chair', data=df)
    plt.xticks(rotation=90)
    plt.ylabel("Positivity Total")
    plt.title("Positivity Total by meeting")
    plt.show()
    plt.close()


def plot_score_positivity_difference(df):

    sns.relplot(x='Date', y='Score_Pos', hue='Chair', data=df)
    plt.xticks(rotation=90)
    plt.ylabel("Difference Positivity")
    plt.title("Difference Positivity by meeting (chair score - total score)")
    plt.show()
    plt.close()



"""
Main
"""

liste_score_hawish = list()

for statement in df.statement:


	if type(statement) == str:
		liste_score_hawish.append(compute_hawkish_score(statement.split(" ")))

	else:
		liste_score_hawish.append(0)



df["score_hawkish"] = liste_score_hawish



"""
df.to_csv(project_directory + "csv_files/" + "final_df_v3.csv")
"""


liste_score_pos_chair = list()
liste_score_postotal = list()
list_chair = list()

for date in df.Date.unique():

	df_date = df[df.Date == date]
	chair_in_charge = df_date.chair_in_charge.unique()[0]
	list_chair.append(chair_in_charge)

	df_date_chair = df_date[df_date.interlocutor_name == chair_in_charge]

	big_statement = list()
	statement_chair = list()

	score_chair_for_statement = list()
	score_total_for_statement = list()


	for statement in df_date_chair.statement:
		if type(statement) == str:
			score_chair_for_statement.append(compute_positivity(statement.split(" ")))
		else:
			pass

	for statement in df_date.statement:
		if type(statement) == str:
			score_total_for_statement.append(compute_positivity(statement.split(" ")))
		else:
			pass

	liste_score_postotal.append( sum(score_total_for_statement) / len(score_total_for_statement) )





liste_score_hawkish_total = list()




for date in df.Date.unique():

	df_date = df[df.Date == date]
	chair_in_charge = df_date.chair_in_charge.unique()[0]
	df_date_chair = df_date[df_date.interlocutor_name == chair_in_charge]

	big_statement = list()
	statement_chair = list()

	for statement in df_date_chair.statement:

		if type(statement) == str:
			for word in statement.split(" "):
				statement_chair.append(word)
		else:
			pass


	for statement in df_date.statement:

		if type(statement) == str:
			for word in statement.split(" "):
				big_statement.append(word)
		else:
			pass


	liste_score_hawkish_total.append(compute_hawkish_score(big_statement))
	



"""
list_difference = list()

for ii in range(len(liste_score_hawkish_chair)):
	list_difference.append(liste_score_hawkish_chair[ii] - liste_score_hawkish_total[ii])
"""



array_score_pos_total = np.array(liste_score_postotal)
array_score_hawish_total = np.array(liste_score_hawkish_total)


corr = np.corrcoef(array_score_pos_total, array_score_hawish_total)



print("la correlation est de :", corr)

"""
list_difference = list()

for ii in range(len(liste_score_postotal)):
	list_difference.append(liste_score_pos_chair[ii] - liste_score_postotal[ii])


liste_date = df.Date.unique()

liste_true_date = list()

for ele in liste_date:
	liste_true_date.append(datetime.datetime.strptime(ele, '%Y-%m-%d'))




df_plot_chair = pd.DataFrame(list(zip(liste_true_date, list_chair, liste_score_pos_chair)), 
               columns =['Date', 'Chair', 'Score_Pos']) 

df_plot_total = pd.DataFrame(list(zip(liste_true_date, list_chair, liste_score_postotal)), 
               columns =['Date', 'Chair', 'Score_Pos']) 

df_plot_difference = pd.DataFrame(list(zip(liste_true_date, list_chair, list_difference)), 
               columns =['Date', 'Chair', 'Score_Pos']) 
"""













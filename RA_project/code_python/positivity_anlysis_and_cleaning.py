
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import ast
from gensim.parsing.preprocessing import STOPWORDS
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.stem import WordNetLemmatizer 
import datetime
import seaborn as sns


stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer() 



"""
Dates and dico
"""

df_sentiment = pd.read_excel('/Users/etiennelenaour/Desktop/Stage/vocab_sentiment.xlsx')

project_directory = '/Users/etiennelenaour/Desktop/Stage/'
l_month = ['January','February','March','April','May','June','July','August','September','October','November','December']
l_dates = list()


with open ('/Users/etiennelenaour/Desktop/Stage/csv_files/dates_fomc.csv', 'r') as doc :
    head = doc.readline()
    dates = doc.readlines()
    dates_to_chg = []
    for line in dates :
        if line.split(',')[1] == ' Y' :
            dates_to_chg += [line.split(';')[0]]
            date = 0
            m = 1   
            for month in l_month :
                if month[:3] == line.split(';')[0].split('/')[0] :
                    date += 100 * m
                m += 1
            date += int(line.split(',')[0].split('/')[2])*10000
            date += int(line.split(',')[0].split('/')[1])
            l_dates.append(date)

l_dates_final = l_dates[1:]

date_to_append = [20120125, 20120425, 20120620, 20120801, 20120913, 20121024, 20121212, 20130130,
20130130, 20130320, 20130501, 20130619, 20130918, 20131030, 20131218, 20140129,
20140129, 20140319, 20140430, 20140618, 20140917, 20141029, 20141217]


for date in date_to_append:
    l_dates_final.append(date)


"""
cleaning functions
"""


def clean_dico_new_line(dico):

	new_dico = defaultdict(lambda: list())

	for keys, list_dico in dico.items():

		new_liste = [string.rstrip("\\n").lower() for string in list_dico]
		new_dico[keys] = new_liste


	return new_dico


def remove_stop_word(dico):


	new_dico = defaultdict(lambda: list())

	for keys, list_dico in dico.items():

		final_list = list()

		for ele in list_dico:

		    if (ele not in STOPWORDS) and (ele not in stop_words):
		        final_list.append(ele)

		new_dico[keys] = final_list

	return new_dico


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




def compute_affirmation_without_chair(dico):

    strong_score = 0
    weak_score = 0

    for liste in list(dico.values())[1:]:

        for ele in liste:

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



def compute_positivity(dico):

	neg_score = 0
	pos_score = 0

	for liste in dico.values():

		for ele in liste:

			if ele in negative_word_list:
				neg_score += 1

			elif ele in positive_word_list:
				pos_score += 1


			else:
				pass

	score = (pos_score - neg_score) / (pos_score + neg_score)

	return score


def compute_affirmation(dico):

	strong_score = 0
	weak_score = 0

	for liste in dico.values():

		for ele in liste:

			if ele in strong_word_list:
				strong_score += 1

			elif ele in weak_word_list:
				weak_score += 1


			else:
				pass

	score = (strong_score - weak_score) / (strong_score + weak_score)

	return score


def compute_uncertainly(dico):

	uncertainly_score = 0
	total_score = 0

	for liste in dico.values():

		for ele in liste:

			total_score += 1

			if ele in uncertainly_word_list:
				uncertainly_score += 1


			else:
				pass

	score = uncertainly_score / total_score

	return - score

def compute_positivity_indiv(dico):

    neg_score = 0
    pos_score = 0

    
    for ele in list(dico.values())[0]:

        if ele in negative_word_list:
            neg_score += 1

        elif ele in positive_word_list:
            pos_score += 1


        else:
             pass

    score = (pos_score - neg_score) / (pos_score + neg_score)

    return score


def compute_affirmation_indiv(dico):

    strong_score = 0
    weak_score = 0

    for ele in list(dico.values())[0]:

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


def compute_uncertainly_indiv(dico):

	uncertainly_score = 0
	total_score = 0

	for ele in list(dico.values())[0]:

		total_score += 1

		if ele in uncertainly_word_list:
			uncertainly_score += 1

		else:
			pass

	score = uncertainly_score / total_score

	return - score


def compute_positivity_for_each(dico, date):

    liste_name = list()
    liste_score = list()
    liste_chair = list()

    for key, value in dico.items():

        neg_score = 0
        posi_score = 0

        
        for ele in value:

            if ele in positive_word_list:
                posi_score += 1

            elif ele in negative_word_list:
                neg_score += 1


            else:
                 pass


        if posi_score > 0 or neg_score > 0:
            score = (posi_score - neg_score) / (posi_score + neg_score)

        else:
            score = 0

        liste_name.append(key)
        liste_score.append(score) 
        
    liste_chair = [list(dico.keys())[0] for ii in range(len(liste_score))] 
    liste_date = [date for ii in range(len(liste_score))]

    dico_score = {"Score" : liste_score, "Name" : liste_name, "Date" : liste_date, "Chair" : liste_chair}

    df_score = pd.DataFrame.from_dict(dico_score)

    return df_score


def compute_affirmation_for_each(dico, date):


    liste_name = list()
    liste_score = list()
    liste_chair = list()

    for key, value in dico.items():

        weak_score = 0
        strong_score = 0

        
        for ele in value:

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

        liste_name.append(key)
        liste_score.append(score) 
        
    liste_chair = [list(dico.keys())[0] for ii in range(len(liste_score))] 
    liste_date = [date for ii in range(len(liste_score))]

    dico_score = {"Score" : liste_score, "Name" : liste_name, "Date" : liste_date, "Chair" : liste_chair}

    df_score = pd.DataFrame.from_dict(dico_score)

    return df_score

def compute_incertitude_for_each(dico, date):


    liste_name = list()
    liste_score = list()
    liste_chair = list()

    for key, value in dico.items():

        incertitude_score = 0
        total_score = 0
             
        for ele in value:

            total_score += 1

            if ele in uncertainly_word_list:
                incertitude_score += 1


            else:
                 pass


        if incertitude_score > 0:
            score = incertitude_score / total_score

        else:
            score = 0

        liste_name.append(key)
        liste_score.append(score) 
        
    liste_chair = [list(dico.keys())[0] for ii in range(len(liste_score))] 
    liste_date = [date for ii in range(len(liste_score))]

    dico_score = {"Score" : liste_score, "Name" : liste_name, "Date" : liste_date, "Chair" : liste_chair}

    df_score = pd.DataFrame.from_dict(dico_score)

    return df_score



"""
Plot fonctions
"""

def from_int_dates(integ):
    string = str(integ)
    new_string = string[0]+ string[1] + string[2] + string[3] + "/" + string[4] + string[5] + "/" + string[6] + string[7]

    return datetime.datetime.strptime(new_string, "%Y/%m/%d") 




def plot_nb_total(df):

    sns.lineplot(x='Date', y='Score_incertitude_relatif', hue='chair_name', data=df)
    plt.grid()
    plt.xticks(rotation=90) 
    plt.ylabel("Score d'incertitude relatif")
    plt.title("Score d'incertitude relatif du chair par rapport au score d'incertitude global")
    plt.show()
    plt.close()


"""
Indiv Plot
"""

def plot_nb_total_second(df):

    sns.lineplot(x='Date', y='Score_incertitude', hue='chair_name', data=df)
    plt.grid()
    plt.xticks(rotation=90)
    plt.ylabel("Score d'incertitude")
    plt.title("Score d'incertitude à travers le temps")
    plt.show()
    plt.close()







"""
Main
"""
list_chair = list()
list_dates = list()

list_score_posi = list()
list_score_affirmation = list()
list_score_incertitude = list()

list_score_posi_chair = list()
list_score_affirmation_chair = list()
list_score_incertitude_chair = list()

list_score_affirmation_without_chair = list()


liste_df = list()


for date in l_dates_final:

    with open (project_directory+'sentences_by_names/'+str(date)+'meeting.txt', 'r') as doc:
        content = doc.readlines()[0]
	    
    dictionary = ast.literal_eval(content)

	#Cleaning 
    dico_clean = remove_stop_word(clean_dico_new_line(dictionary))




	#Compute score and append date liste
    
    df = compute_incertitude_for_each(dico_clean, from_int_dates(date))
    liste_df.append(df)
    

    """
    list_chair.append(list(dico_clean.keys())[0])
    
    list_dates.append(from_int_dates(date))
    list_score_incertitude.append(compute_uncertainly(dico_clean))
    list_score_incertitude_chair.append(compute_uncertainly_indiv(dico_clean))
    
    list_score_affirmation_without_chair.append(compute_affirmation_without_chair(dico_clean))
	
    list_score_posi_chair.append(compute_positivity_indiv(dico_clean))
    list_score_affirmation.append(compute_affirmation(dico_clean))
    list_score_posi.append(compute_positivity(dico_clean))
    list_score_affirmation.append(compute_affirmation(dico_clean))
    list_score_incertitude.append(compute_uncertainly(dico_clean))
    
    """

df_finale_score = pd.concat(liste_df, axis = 0)
print(df_finale_score)
df_finale_score.to_csv(project_directory + "csv_files/" + "df_score_incertitude_finale.csv")



"""
Score_incertitude_relatif = list()

for i in range(len(list_score_incertitude)):
    Score_incertitude_relatif.append(list_score_incertitude_chair[i] / list_score_incertitude[i])


df = pd.DataFrame(list(zip(list_dates, Score_incertitude_relatif, list_chair)), columns = ['Date', 'Score_incertitude_relatif', 'chair_name'])

df1 = df[df.chair_name != 'MR. PARDEE.']
df2 = df1[df1.chair_name != 'VICE CHAIRMAN SOLOMON.']
df3 = df2[df2.chair_name != 'VICE CHAIRMAN DUDLEY.']

plot_nb_total(df3)

df4 = pd.DataFrame(list(zip(list_dates, list_score_incertitude, list_chair)), columns = ['Date', 'Score_incertitude', 'chair_name'])
df5 = df4[df4.chair_name != 'MR. PARDEE.']
df6 = df5[df5.chair_name != 'VICE CHAIRMAN SOLOMON.']
df7 = df6[df6.chair_name != 'VICE CHAIRMAN DUDLEY.']


plot_nb_total_second(df7)




df_chairman = pd.DataFrame(list(zip(list_dates,list_chair)), columns = ['Date', 'ChairName'])
df_chairman.to_csv(project_directory + "csv_files/" + "df_chairman.csv")

#df_affirmation = pd.DataFrame(list(zip(list_dates, list_score_affirmation_without_chair, list_score_posi)),
    #columns = ['Date', 'ScoreAffiWithoutChair', 'ScorePosti'])

#df_affirmation.to_csv(project_directory + "csv_files/" + "df_affirmation.csv")

df_score = pd.DataFrame(list(zip(list_dates, list_score_incertitude, list_score_posi, list_score_affirmation)), \
    columns =['Date', 'ScoreIncert', 'ScorePosti', 'ScoreAffi']) 

df_score.to_excel(project_directory + "csv_files/" + "df_score_sentiment.xlsx")


#plot_posi_indiv(list_dates, list_score_posi_chair, list_score_posi)
"""




    
    




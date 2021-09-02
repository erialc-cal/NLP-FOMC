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
import json

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer




##################
#Fonctions#
##################

def remove_name_in_list(name, liste):

	if len(name.split(" ")) == 3:
		part_one, part_two, part_three = name.split(" ")

	else :
		part_one, part_two = name.split(" ")
		part_three = None


	liste_filter = [ele for ele in liste if ele != part_one and ele != part_two and ele != part_three]

	return liste_filter


def RemoveBadCarac(mot):
    """
    remove a list of bad carac in a word
    """
    bad_carac = [",", "*", "'", "]", "[", "-", "!", "?", " ", '', "(", ")", "//", ".", '-']
    mot_propre = list()
    for carac in mot:
        if carac not in bad_carac and not carac.isnumeric():
            mot_propre.append(carac)
        else:
            mot_propre.append("")
    #return mot
    return("".join(mot_propre))



def Create_and_fill_dict_by_name(liste_of_dico):

	cleaning_list = ["think", "yes", "bee", "ca", "dont", "mr", "ms", "tha", 'yes', "like",
	 "point", "say", "im"]

	big_dico = defaultdict(lambda: list())

	for dico in liste_of_dico:

		for key, liste in dico.items():

			for ele in remove_name_in_list(key, liste):

				alphanumeric_filter = filter(str.isalnum, ele)
				ele_clean = "".join(alphanumeric_filter)

				if ele_clean != "" and ele_clean not in cleaning_list:
					big_dico[key].append(ele_clean)

	return big_dico


##################
#Gestion de dates#
##################




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





#############
#MAIN########
#############

liste_dico = list()


for date in l_dates_final:

    with open (project_directory+'sentences_by_names/'+str(date)+'meeting.txt', 'r') as doc:
        content = doc.readlines()[0]
	    
    dictionary = ast.literal_eval(content)

	#Cleaning 
    liste_dico.append(dictionary)
	#Compute score and append date liste




dico_person = Create_and_fill_dict_by_name(liste_dico)


#############
#Prepare LDA#
#############

def from_dico_to_df(dico):


	liste_key = list()
	liste_texte = list()

	for key, liste in dico.items():
		liste_key.append(key)
		texte = " ".join(liste)
		liste_texte.append(texte)


	df_texte = pd.DataFrame(list(zip(liste_key, liste_texte)), columns =['interlo', 'texte']) 

	return df_texte


df_texte = from_dico_to_df(dico_person)

chair_name = ['CHAIRMAN BURNS.', 'CHAIRMAN MILLER.', 'CHAIRMAN VOLCKER.', 'CHAIRMAN GREENSPAN.', 'CHAIRMAN BERNANKE.', 'CHAIR YELLEN.']
chair_name_idx = [0, 48, 65, 138, 267, 373]

#############
#LDA########
#############


n_top_words = 20

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()


tf_vectorizer = CountVectorizer(max_df=0.90, min_df=0.05, stop_words='english')


tf = tf_vectorizer.fit_transform(df_texte['texte'])



lda = LatentDirichletAllocation(n_components=5, max_iter=10,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)



lda.fit(tf)

print("\nTopics in LDA model:")
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)


doc_topic = lda.transform(tf)

for ii in range(len(chair_name)):
	print("Pour le chair :", chair_name[ii],", voici la distribution des topics : ", doc_topic[chair_name_idx[ii]])










###############
##Some imports#
###############
import datetime
import matplotlib.pyplot as plt
import ast
from collections import OrderedDict 
from collections import defaultdict
import seaborn as sns
import pandas as pd

###############
##Global variables#
###############

project_directory = '/Users/etiennelenaour/Desktop/Stage/'
l_month = ['January','February','March','April','May','June','July','August','September','October','November','December']
l_dates = list()




#######################
#Descriptive fonctions#
#######################

def count_words(dico):

    dico_counts = defaultdict(lambda: list())

    for speaker, liste_word in dico.items(): 
    
        dico_counts[speaker] = len(liste_word)

    return dico_counts


def count_total_words(dico):

    return sum(list(dico.values()))



def from_int_dates(integ):
    string = str(integ)
    new_string = string[0]+ string[1] + string[2] + string[3] + "/" + string[4] + string[5] + "/" + string[6] + string[7]

    return datetime.datetime.strptime(new_string, "%Y/%m/%d")   





def plot_nb_total(df):

    sns.scatterplot(x='Date', y='nb_mot_relatif', hue='chair_name', data=df)
    plt.grid()
    plt.xticks(rotation=90)
    plt.ylabel("Ratio")
    plt.title("Ratio du nombre de mots prononcés par le CHAIRMAN")
    plt.show()
    plt.close()



#######################
#main##################
#######################



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
            

l_dates_final = l_dates[2:]

date_to_append = [20120125, 20120425, 20120620, 20120801, 20120913, 20121024, 20121212, 20130130,
20130130, 20130320, 20130501, 20130619, 20130918, 20131030, 20131218, 20140129,
20140129, 20140319, 20140430, 20140618, 20140917, 20141029, 20141217]

for date in date_to_append:
    l_dates_final.append(date)



list_nb_mot_chairman = list()
list_dates = list()
list_nb_mot_total = list()
list_chair_name = list()



for date in l_dates_final:
    with open (project_directory+'sentences_by_names/'+str(date)+'meeting.txt', 'r') as doc:
        content = doc.readlines()[0]
        dictionary = ast.literal_eval(content)
        nb_word_dico = count_words(dictionary)


    list_nb_mot_total.append(count_total_words(nb_word_dico))
    list_nb_mot_chairman.append(list(nb_word_dico.values())[0])
    list_dates.append(from_int_dates(date))
    list_chair_name.append(list(dictionary.keys())[0])


new_list = list()

for i in range(len(list_nb_mot_chairman)):
        new_list.append(list_nb_mot_chairman[i] / list_nb_mot_total[i])


df = pd.DataFrame(list(zip(list_dates, new_list, list_chair_name)), columns =['Date', 'nb_mot_relatif', 'chair_name']) 
df1 = df[df.chair_name != 'MR. PARDEE.']
df2 = df1[df1.chair_name != 'VICE CHAIRMAN SOLOMON.']
df3 = df2[df2.chair_name != 'VICE CHAIRMAN DUDLEY.']




df4 = df3[['chair_name', 'nb_mot_relatif']]
print(df4.groupby(['chair_name']).nb_mot_relatif.agg(['mean', 'std']))






        
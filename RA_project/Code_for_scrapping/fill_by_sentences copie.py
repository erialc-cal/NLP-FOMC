##################
#Some Imports#####
##################

from collections import defaultdict
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import datetime
import os
dir_name = os.path.dirname(__file__)


project_directory = dir_name
##################
#Global variables#
##################


l_month = ['January','February','March','April','May','June','July','August','September','October','November','December']

with open(project_directory+'/transcript_files_txt/scrapped_dates.txt', 'r') as f:
    l_dates = f.read().splitlines()


##################
#functions########
##################

def IsWordInCapital(word):
    """
    Test if word is in capital
    """
    boo = True

    if len(word)>1 :
        for letter in word[:-1]:


            if letter.isupper():
                pass
            else:
                boo = False
    else:
        boo = False

    return boo



def RemoveBadCarac(mot):
    """
    remove a list of bad carac in a word
    """
    bad_carac = [",", "*", "'", "]", "[", "-", "!", "?", " ", '', "(", ")", "//", ".", '-', '\\n', '$', '€']
    mot_propre = list()
    for carac in mot:
        if carac not in bad_carac and not carac.isnumeric():
            mot_propre.append(carac)
        else:
            mot_propre.append("")
    #return mot
    return("".join(mot_propre))




def get_names(statements):

    '''
    take statements inputs return list of names
    '''

    list_names = list()
    names_position = list()

    list_prefixe = ['CHAIRMAN', 'MR', 'MS', 'VICE CHAIRMAN', 'CHAIR']


    for ii in range(len(statements)):

        if statements[ii] in list_prefixe:

            
            if statements[ii-1] == 'VICE':
                list_names.append(statements[ii-1] + ' ' + statements[ii] \
                    + ' ' + statements[ii+1])

                names_position.append(ii-1)

            elif IsWordInCapital(statements[ii+1]):
                list_names.append(statements[ii] + ' ' + statements[ii+1])

                names_position.append(ii)

            else: 
                pass


        else:
            pass



    return list_names, names_position



def get_sentences_by_name(statements):

    list_names, names_position = get_names(statements)

    dico_sentences_by_name = defaultdict(lambda: list())

    liste_finale, liste_statement = list(), list()

    for ii in range(len(names_position)-1):

        liste_inter = [list_names[ii], int(names_position[ii+1] - names_position[ii] - 2)]
        liste_finale.append(liste_inter)

        liste_inter_statement = list()
        
        for jj in range(names_position[ii], names_position[ii+1], 1):


            #Ici on nettoye

            dico_sentences_by_name[list_names[ii]].append(RemoveBadCarac(statements[jj]))
            liste_inter_statement.append(RemoveBadCarac(statements[jj]))

        liste_statement.append(" ".join(liste_inter_statement[2:]))
            




    for name in set(list_names):
        dico_sentences_by_name[name] = clean_list(dico_sentences_by_name[name])
        dico_sentences_by_name[name] = list(filter(None, dico_sentences_by_name[name]))

    return dico_sentences_by_name, liste_finale, liste_statement



def from_liste_to_df(liste, date, liste_statement):

    name_list, size_list = list(), list()

    for sub_list in liste:
        name_list.append(sub_list[0])        
        size_list.append(sub_list[1])

    df_length_statement = pd.DataFrame(list(zip(name_list, size_list, liste_statement)), columns =['interlocutor_name', 'statement _size', "statement"]) 
    df_length_statement["statement_number"]= ["statement_" + str(ii) for ii in range(len(df_length_statement.index))]
    df_length_statement["Date"] = [from_int_dates(date) for ii in range(len(df_length_statement.index))]

    chair_name = ['CHAIRMAN BURNS', 'CHAIRMAN MILLER', 'CHAIRMAN VOLCKER', 'CHAIRMAN GREENSPAN', 'CHAIRMAN BERNANKE', 'CHAIR YELLEN']

    the_chair = "None"

    for name in name_list:
        for chair in chair_name:
            if name == chair:
                the_chair = name
            else:
                pass
        else:
            pass

    the_chair_liste = [the_chair for ii in range(len(name_list))]

    df_length_statement["chair_in_charge"] = the_chair_liste


    return df_length_statement



########################
##Fonction de nettoyage#
########################

def from_int_dates(integ):
    string = str(integ)
    new_string = string[0]+ string[1] + string[2] + string[3] + "/" + string[4] + string[5] + "/" + string[6] + string[7]

    return datetime.datetime.strptime(new_string, "%Y/%m/%d") 
    
    
    
def RemoveBadCarac2(mot):
    """
    remove a list of bad carac in a word
    """
    bad_carac = [",", "*", "'", "]", "[", "-", " ", '', "(", ")", "//", "\\", "\"", ".", "_"]
    mot_propre = list()

    for carac in mot:
        if carac not in bad_carac and not carac.isnumeric():
            mot_propre.append(carac)
        else:
            pass
    #return mot
    return("".join(mot_propre))



def clean_list(liste):

    clean = list()
    word_to_remove =  ["unintelligible", "speaker", "mr", "im", ":", "of", "wouldnt", "didnt", "doesnt",\
     "dont", "id", "im", "ive", "okay", "thats", "weve", "worker", "wouldnt", "yield", "youre", "theyre", "whats"]

    for ele in liste:
        if ele not in word_to_remove:
            clean.append(RemoveBadCarac(ele).rstrip("\u2019"))
        else:
            pass

    return clean


##################
#Plot#############
##################

def plot_speak(liste, date):

    nom_chair = str()
    x_liste = list()
    y_liste = list()

    boo_nom_chair = True
    
    for sublist in liste:
        x_liste.append(sublist[0])
        y_liste.append(sublist[1])

    x_true_liste = list()

    for ele in x_liste:

        if ele[:5] == 'CHAIR':
            x_true_liste.append('CHAIR')

            if boo_nom_chair:
                nom_chair = ele
                boo_nom_chair = False

            else:
                pass

        else:
            x_true_liste.append('Autre')


    x_chair = list()
    y_chair = list()

    x_non_chair = list()
    y_non_chair = list()

    for ii in range(len(x_true_liste)):

        if x_true_liste[ii] == 'CHAIR':
            x_chair.append(ii)
            y_chair.append(y_liste[ii])

        elif x_true_liste[ii] == 'Autre':
            x_non_chair.append(ii)
            y_non_chair.append(y_liste[ii])

        else:
            pass


    plt.figure(figsize=(20,7))

    plt.subplot(211)
    plt.bar(x_chair, y_chair,  color='b', label='CHAIR')
    plt.title("Taille et moment des interventions des intervenants : Pour la réunion {0} et {1}".format(date, nom_chair))
    plt.xlabel("Numéro de la phrase dans l'ordre chronologique")
    plt.ylabel("Taille de l'intervention en nombre de mots")
    plt.legend()

    plt.subplot(212)
    plt.bar(x_non_chair, y_non_chair, color='r', label='OTHERS')

    plt.legend()
    
    plt.savefig(project_directory + '/image_chair_temp/' + 'chair_tempo_' + str(date) + '.png')
    plt.close()



"""
    sns.barplot(x = x_liste, y = y_liste)
    plt.grid()
    plt.xticks(rotation=90)
    plt.ylabel("Taille des interventions en mot")
    plt.title("Interventions au cours de la réunion : " + date)
    plt.tight_layout()
    plt.show()
    plt.close()
"""




##################
#Date#############
##################

# with open ('/Users/etiennelenaour/Desktop/Stage/csv_files/dates_fomc.csv', 'r') as doc :
#     head = doc.readline()
#     dates = doc.readlines()
#     dates_to_chg = []
#     for line in dates :
#         if line.split(',')[1] == ' Y' :
#             dates_to_chg += [line.split(';')[0]]
#             date = 0
#             m = 1   
#             for month in l_month :
#                 if month[:3] == line.split(';')[0].split('/')[0] :
#                     date += 100 * m
#                 m += 1
#             date += int(line.split(',')[0].split('/')[2])*10000
#             date += int(line.split(',')[0].split('/')[1])
#             l_dates.append(date)
            

# l_dates_final = l_dates

# date_to_append = [20120125, 20120425, 20120620, 20120801, 20120913, 20121024, 20121212, 20130130,
# 20130130, 20130320, 20130501, 20130619, 20130918, 20131030, 20131218, 20140129,
# 20140129, 20140319, 20140430, 20140618, 20140917, 20141029, 20141217]

# for date in date_to_append:
#     l_dates_final.append(date)

l_dates_final = l_dates

##################
#Main#############
##################


df_statement_size_list = list()
liste_chair_in_charge = list()
liste_statement = list()




for date in l_dates_final[1:]:

    with open (project_directory+'/transcript_files_txt/'+str(date)+'meeting.txt', 'r') as doc:
        
        content = [str(ele.split(' ')[0]) for ele in doc.read().splitlines()]
        #content = doc.readlines()[0]
        
        #content_bis = content.split("\n")
   
        new_string = " ".join(content)
        liste_word = new_string.split(" ")

        bad_carac = [",", "*", "'", "]", "[", "-", " ", '', "(", ")", "//", ".", '-', '$', '€', "/", ";", "Š", "™", "."]

        good_liste = list()

        for ele in liste_word:
            
            word = list()
            
            for carac in ele:
                if carac not in bad_carac:
                    word.append(carac)
                else:
                    pass
                
            good_liste.append("".join(word))
            
        filter_list = list(filter(None, good_liste))

        useless, liste_finale, liste_statement = get_sentences_by_name(filter_list) 

        df_statement_size_list.append(from_liste_to_df(liste_finale, date, liste_statement))



df_statement_size = pd.concat(df_statement_size_list)
path_to_save = project_directory + "/df_statement_real.csv"
df_statement_size.set_index("Date").to_csv(path_to_save)




"""
with open(project_directory+'transcript_short_version_txt/'+str(l_dates_final[300])+'clean_meeting.txt', 'r') as doc:
        content = doc.readlines()[0].split(' ')

content_clean = list(filter(None, clean_list(content)))
print(get_sentences_by_name(content_clean)[1])
"""

"""
for date in l_dates_final[1:]:

    with open (project_directory+'transcript_short_version_txt/'+str(date)+'clean_meeting.txt', 'r') as doc:
        content = doc.readlines()[0].split(' ')
        

    with open(project_directory+'sentences_by_names/'+str(date)+'meeting.txt', 'w') as sortie:
        json.dump(get_sentences_by_name(content)[0], sortie)
        
"""

 



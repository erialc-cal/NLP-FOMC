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
from tqdm import trange
import re
dir_name = os.path.dirname(__file__)


project_directory = dir_name

#%%
##################
#Global variables#
##################




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
    bad_carac = [",", "*", "'", "]", "[", "-", " ", 
                 '', "(", ")", "//", '-', '\\n', 
                 'Š','Œ','™','ﬁ','ﬂ','í' ]
    mot_propre = list()
    for carac in mot:
        if carac not in bad_carac: #and not carac.isnumeric():
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

    list_prefixe = ['CHAIRMAN', 'MR.', 'MS.', 'VICE CHAIRMAN', 'CHAIR', 'MR', 'MS']


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



#%% TESTS

date = '20140730'
file1 = open(project_directory+'/transcript_files_txt/'+str(date)+'meeting.txt', 'r')
def clean_text_before_search(file1):
    lines = file1.readlines()
    lines_cleaned=""
    
    
    for i in trange(len(lines)):
        line = lines[i]
        line_s = ""
        for word in line.split() : 
            word = RemoveBadCarac(word)
            line_s += ' '+word
        lines_cleaned+=line_s
    return lines_cleaned
            

            
def find_meeting_start(lines_cleaned):
    """ function that searches for the start of the meeting
    returns the raw position of the document seen as a string, to use after clean_text_before_search """
    
    start_pos, start = 0, 0
    pattern='Transcript of the Federal Open Market Committee Meeting'
    if re.search(pattern, lines_cleaned):
        print('found a match !')
        start_pos = re.search(pattern, lines_cleaned).span()[1]
    pattern2 = 'Session'
    if re.search(pattern2, lines_cleaned[start_pos:]):
        start = re.search(pattern2, lines_cleaned[start_pos:]).span()[1]
    return start_pos+start+1



def check_broken_words(cleaned_lines):
    """
    Méthode sommaire pour bricoler les mots tronqués par sauts de ligne ou autre dans la conversion pdf 
    """
    not_broken_words = ['a', 'i','im', 'if','it','s', 're','d','ll','ve', 'id','is', 'or','he','ex', 
                        'be','in', 'at', 'to', 'ok', 'on', 'so', 'us', 'up', 'hi', 'by', 'b',
                        'as','me', 'my', 'we','mr', 'ms', 'do', 'go', 'no', 'am', 'of', "an",'ct', 'oh']
    
    word_list = cleaned_lines.lower().split()
    clean = ""
    for i in trange(len(word_list)):
        words = word_list[i]
        if len(words)<=2 and words not in not_broken_words and words.isnumeric()== False:
            #print(words, word_list[i+1], word_list[i-1])
            n, m = len(word_list[i-1]), len(word_list[i+1])
            if n < m:
                clean+= word_list[i-1]+words+' '
            else :
                clean += words+word_list[i+1]+' '
        else : 
            clean+=words+' '
    return clean

#TEST

# lines_c = clean_text_before_search(file1)


# c = check_broken_words(lines_c)


def main_dataframe_constructor(l_dates):
    """
    Deprecated, use main_dataframe_constructor2

    Parameters
    ----------
    l_dates : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    l_dates_final = l_dates
    
    ##################
    #Main#############
    ##################
    
    
    df_statement_size_list = list()
   # liste_chair_in_charge = list()
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
    



#%%


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
def main_dataframe_constructor2(l_dates):
    """
    Crreates updated dataframe with transcript statement, statement size, statement size, chair in charge and interlocutor's name

    Parameters
    ----------
    l_dates : list of dates for scrapping data

    Returns
    -------
    None.

    """
    l_dates_final = l_dates
    
    ##################
    #Main#############
    ##################
    
    
    df_statement_size_list = list()
    #liste_chair_in_charge = list()
    liste_statement = list()
    
    
    
    
    for date in l_dates_final[1:]:
        # opening file
        file1 = open (project_directory+'/transcript_files_txt/'+str(date)+'meeting.txt', 'r')
        # cleaning file
        lines_cleaned = clean_text_before_search(file1)
        
        # getting the statements (ignoring introduction of participants etc.)
        start = find_meeting_start(lines_cleaned)
        statements =lines_cleaned[start:].split()
        
        # creating the by name dictionary of each statement
        dico_sentences_by_name, liste_finale, liste_statement = get_sentences_by_name(statements)

        df_statement_size_list.append(from_liste_to_df(liste_finale, date, liste_statement))
    
    
    
    df_statement_size = pd.concat(df_statement_size_list)

    #want to save in the directory to add scores

    path_to_save = os.path.dirname(os.path.abspath(project_directory) + "score_computing/scrapped_cleaned.csv"
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

 



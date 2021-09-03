

#some import
import os
dir_name = os.path.dirname(__file__)


project_directory = dir_name


from gensim.parsing.preprocessing import STOPWORDS
from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer 


stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer() 


# project_directory = '/Users/etiennelenaour/Desktop/Stage/'

#l_month = ['January','February','March','April','May','June','July','August','September','October','November','December']

#l_dates = list()

l_dates = [20120125, 20120312, 20120425, 20120620, 20120801, 20120913, 20121024, 20121212,
20130130, 20130320, 20130501, 20130619, 20130918, 20131016, 20131030, 20131218,
20140129, 20140304, 20140319, 20140430, 20140618, 20140630, 20140917, 20141029, 20141217]

def IsWordToRemove(word):
    """
    Test if word is in capital
    """
    boo = True

    if len(word)>2 or word=='MR':
        for letter in word[:-1]:


            if letter.isupper():
                pass
            else:
                boo = False
    else:
        boo = False

    return boo


def IsDate(word):
    """
    Test if word is a date
    """
    boo = False
    if len(word) > 7:
        if (word[-3] == "/") and (word[-6]=="/"):
            boo = True
        else:
            pass
    else:
        pass

    return boo


def OwnBracket(word):
    """
    Test if word is beetween bracket
    """
    boo = False
    if len(word) > 1:
        if word[-1] == "]" or word[0] == "[":
            boo = True
        else:
            pass
    else:
        pass

    return boo
    
    
    
def RemoveBadCarac(mot):
    """
    remove a list of bad carac in a word
    """
    bad_carac = [",", "*", "'", "]", "[", "-", ".", "!", "?", " ", '', "(", ")"]
    mot_propre = list()
    for carac in mot:
        if carac not in bad_carac and not carac.isnumeric():
            mot_propre.append(carac)
        else:
            pass
    #return mot
    return("".join(mot_propre))




#Initialisation de la liste date a l'aide du fichier csv
"""
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
"""



for date in l_dates[1:]:

    with open (project_directory+'transcript_short_version_txt/'+str(date)+'clean_meeting.txt', 'r') as doc:
        
        list_word = [ele.split(' ') for ele in doc.readlines()[0].split('\\n')]
        
        flat_list = list()
        for sublist in list_word:
            for item in sublist:
                flat_list.append(item)
        


    word_to_remove =  ["unintelligible", "speaker", "mr", "im", ":", "of", "wouldnt", "didnt", "doesnt",\
     "dont", "id", "im", "ive", "okay", "thats", "weve", "worker", "wouldnt", "yield", "youre", "theyre", "whats"]


    intermed_list = list()
    final_list = list()


    for ele in flat_list:
        if IsWordToRemove(ele) or IsDate(ele) or OwnBracket(ele):
            pass
        else:
            ele_to_add = ele.lower().replace(' ', '')
            intermed_list.append(RemoveBadCarac(ele_to_add))



    for ele in intermed_list:
        if (ele not in STOPWORDS) and (ele not in stop_words) and (ele not in word_to_remove):
            final_list.append(ele)
        else:
            pass
            
    final_list = list(filter(None, final_list))

    lemmatize_list = [lemmatizer.lemmatize(ele) for ele in final_list]


    with open(project_directory+'transcript_to_word_set/'+str(date)+'meeting.txt', 'w') as sortie:
        sortie.write(" ".join(lemmatize_list))
        sortie.close

    


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 09:18:20 2021

@author: Claire He 

Compute following scores based on Etienne Le Naour's previous work. Score details can be found
in the corresponding pdf file.

Scores computed at the end of the file in a csv file for each statement of the original csv : 
• score posi : positivity score
• score affi : assertion score
• score incert : uncertainty score
• score acadam : academic score
• score hostile : hostility score
• score econo : economy score
• score virtue : virtue score
• score vice : vice score

List of functions to call :
    - add_score_positivity
    - add_score_incertitude
    _ add_score_econo
    _ add_score_affirmation
    _ add_score_academ
    _ add_score_hostile
    _ add_score_virtue_vice
"""

#%% Packages import 
import os
project_directory = os.path.dirname(__file__)
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
import numpy as np

stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer() 

#%% DATA
# DATA : DICTIONARY FOR SENTIMENT ANALYSIS
### First dictionary is Loughran McDonald dictionary --> https://sraf.nd.edu/textual-analysis/resources/
df1 = pd.read_csv(project_directory+'/dico_Loughran_McDo.csv', low_memory=True)
### Second dictionary is from Harvard's spreadsheet --> http://www.wjh.harvard.edu/~inquirer/spreadsheet_guide.htm
df2 = pd.DataFrame(pd.read_excel(project_directory+'/dico_Harvard.xls'))
df2 = df2.iloc[1:] # L'entrée 0 compte le nombre de valeurs de chaque colonne
df2 = df2.replace(np.nan, 0)
df2.Entry = df2.Entry.astype('str')


##### DISCLAIMER ######
# The first dictionary has been modified in 2020, instead of classifying in each column a type for 
# words ordered by alphabetical order, the words are used as index and the different columns
# contain the year in which the word has been added (+) or deleted (-) from each type. 




#%% DICTIONARIES

### LOUGHRAN MC DONALD DICTIONARY 
negative_word_list = [x.lower() for x in df1[df1.Negative > 0].Word.tolist()]
positive_word_list = [x.lower() for x in df1[df1.Positive > 0].Word.tolist()]

weak_modal = [x.lower() for x in df1[df1.Weak_Modal > 0].Word.tolist()]
strong_modal = [x.lower() for x in df1[df1.Strong_Modal > 0].Word.tolist()]

incertitude = [x.lower() for x in df1[df1.Uncertainty > 0].Word.tolist()]
complexity = [x.lower()for x in df1[df1.Complexity > 0].Word.tolist()]

### HARVARD DICTIONARY
academic =  [x.lower() for x in df2[df2.Academ != 0].Entry.tolist()]

hostile = [x.lower() for x in df2[df2.Hostile != 0].Entry.tolist()]

econo = [x.lower() for x in df2[df2['Econ@'] != 0].Entry.tolist()]

virtue = [x.lower() for x in df2[df2.Virtue != 0].Entry.tolist()]

vice = [x.lower() for x in df2[df2.Vice != 0].Entry.tolist()]

# Cleaning statements

def remove_stop_word_per_statement(statement):
    """
    Takes a statement and removes stop words from the gensim parsing package

    Parameters
    ----------
    statement : str

    Returns
    -------
    cleaned statement, str

    """
    clean_statement = ""
    for ele in statement.split():
        if (ele not in STOPWORDS) and (ele not in stop_words):
            clean_statement += ele+' '
    return clean_statement


#%%
# POSITIVITY SCORE

def compute_positivity_per_statement(statement):
    """
    This function computes the positivity score of each statement

    Parameters
    ----------
    statement : str, statement 
    Returns
    -------
    score

    """
    neg_score, pos_score, score = 0,0, 0
    for ii in range(10):
        for ele in statement.lower().split():
            #print(ele)
            if ele in negative_word_list:
                neg_score += 1
            elif ele in positive_word_list:
                pos_score += 1
            else:
                pass
        if neg_score < 30 or pos_score < 30:
            pass
        else:
            score = (pos_score - neg_score) / (pos_score + neg_score)
    
    return score
    
    
# MEAN POSITIVITY

def compute_mean_positivity(statement):
    """
        This function computes the mean positivity score of each statement

    Parameters
    ----------
    statement : str, statement 
    Returns
    -------
    score
    """
    neg_score = 0
    pos_score = 0
    for word in statement.lower().split():
        #print(word)
        if word in negative_word_list :
            neg_score += 1
        elif word in positive_word_list :
            pos_score += 1
        else:
            pass
    if pos_score+neg_score != 0:
        score = (pos_score - neg_score) / (pos_score + neg_score)
    else : 
        score = (pos_score - neg_score)
    return score


def add_score_positivity(df):
    """
    Adds positivity score to the dataset 
    
    """
    score = []
    for statement in df.statement : 
        clean_statement = remove_stop_word_per_statement(statement)
        score.append(compute_mean_positivity(clean_statement))
    df['score_posi']= score
    return df 

#%% AFFIRMATION SCORE 

def compute_mean_affirmation(statement):
    """
        This function computes the mean affirmation score of each statement

    Parameters
    ----------
    statement : str, statement 
    Returns
    -------
    score
    """
    weak_score = 0
    strong_score = 0
    for word in statement.lower().split():
        #print(word)
        if word in weak_modal :
            weak_score += 1
        elif word in strong_modal :
            strong_score += 1
        else:
            pass
    if weak_score+strong_score != 0:
        score = (strong_score - weak_score) / (strong_score + weak_score)
    else : 
        score = (strong_score - weak_score)
    return score

#score_acadam,score_hostile,score_econo,score_virtue,score_vice,score_hawkish,score_posi,score_affi,score_uncert,Affil,Hostile,Strong,Power,Weak,Submit,Active,Passive,Ovrst,Undrst,Quan,ORD,CARD,NUMB,Yes,No,Negate,SureLw,If,NotLw,RspGain,ABS,Causal

def add_score_affirmation(df):
    """
    Adds affirmation score to the dataset 
    
    """
    score = []
    for statement in df.statement : 
        clean_statement = remove_stop_word_per_statement(statement)
        score.append(compute_mean_affirmation(clean_statement))
    df['score_affi']= score
    return df 

#%% Incertitude score

def compute_incertitude(statement):
    """
        This function computes the incertitude score of each statement

    Parameters
    ----------
    statement : str, statement 
    Returns
    -------
    score
    """
    inc_score = 0
    nb_words = len(statement.split())
    for word in statement.lower().split():
        #print(word)
        if word in incertitude :
            inc_score += 1
        else:
            pass
    score = - inc_score/nb_words
    return score

#score_acadam,score_hostile,score_econo,score_virtue,score_vice,score_hawkish,score_posi,score_affi,score_uncert,Affil,Hostile,Strong,Power,Weak,Submit,Active,Passive,Ovrst,Undrst,Quan,ORD,CARD,NUMB,Yes,No,Negate,SureLw,If,NotLw,RspGain,ABS,Causal

def add_score_incertitude(df):
    """
    Adds affirmation score to the dataset 
    
    """
    score = []
    for statement in df.statement : 
        clean_statement = remove_stop_word_per_statement(statement)
        score.append(compute_incertitude(clean_statement))
    df['score_uncert']= score
    return df 

#%% Academic score


def compute_academ(statement):
    """
        This function computes the incertitude score of each statement

    Parameters
    ----------
    statement : str, statement 
    Returns
    -------
    score
    """
    aca_score = 0
    nb_words = len(statement.split())
    for word in statement.lower().split():
        #print(word)
        if word in academic :
            aca_score += 1
        else:
            pass
    score = aca_score/nb_words
    return score

#score_acadam,score_hostile,score_econo,score_virtue,score_vice,score_hawkish,score_posi,score_affi,score_uncert,Affil,Hostile,Strong,Power,Weak,Submit,Active,Passive,Ovrst,Undrst,Quan,ORD,CARD,NUMB,Yes,No,Negate,SureLw,If,NotLw,RspGain,ABS,Causal

def add_score_academ(df):
    """
    Adds academic score to the dataset 
    
    """
    score = []
    for statement in df.statement : 
        clean_statement = remove_stop_word_per_statement(statement)
        score.append(compute_academ(clean_statement))
    df['score_academ']= score
    return df 


#%% Hostile score

def compute_hostile(statement):
    """
        This function computes the hostility score of each statement

    Parameters
    ----------
    statement : str, statement 
    Returns
    -------
    score
    """
    host_score = 0
    nb_words = len(statement.split())
    for word in statement.lower().split():
        #print(word)
        if word in hostile :
            host_score += 1
        else:
            pass
    score = host_score/nb_words
    return score


def add_score_hostile(df):
    """
    Adds hostile score to the dataset 
    
    """
    score = []
    for statement in df.statement : 
        clean_statement = remove_stop_word_per_statement(statement)
        score.append(compute_hostile(clean_statement))
    df['score_hostile']= score
    return df 



#%% Score econo

def compute_econo(statement):
    """
        This function computes the incertitude score of each statement

    Parameters
    ----------
    statement : str, statement 
    Returns
    -------
    score
    """
    eco_score = 0
    nb_words = len(statement.split())
    for word in statement.lower().split():
        #print(word)
        if word in econo :
            eco_score += 1
        else:
            pass
    score = eco_score/nb_words
    return score

#score_acadam,score_hostile,score_econo,score_virtue,score_vice,score_hawkish,score_posi,score_affi,score_uncert,Affil,Hostile,Strong,Power,Weak,Submit,Active,Passive,Ovrst,Undrst,Quan,ORD,CARD,NUMB,Yes,No,Negate,SureLw,If,NotLw,RspGain,ABS,Causal

def add_score_econo(df):
    """
    Adds academic score to the dataset 
    
    """
    score = []
    for statement in df.statement : 
        clean_statement = remove_stop_word_per_statement(statement)
        score.append(compute_econo(clean_statement))
    df['score_econo']= score
    return df 

#%% VIRTUE AND VICE


def compute_virtue_and_vice(statement):
    """
        This function computes the virtue and vice score of each statement

    Parameters
    ----------
    statement : str, statement 
    Returns
    -------
    score
    """
    vir, vic = 0,0
    nb_words = len(statement.split())
    for word in statement.lower().split():
        #print(word)
        if word in virtue :
            vir += 1
        elif word in vice :
            vic +=1
        else:
            pass
    score1 = vic/nb_words
    score2 = vir/nb_words
    return score1, score2

#score_acadam,score_hostile,score_econo,score_virtue,score_vice,score_hawkish,score_posi,score_affi,score_uncert,Affil,Hostile,Strong,Power,Weak,Submit,Active,Passive,Ovrst,Undrst,Quan,ORD,CARD,NUMB,Yes,No,Negate,SureLw,If,NotLw,RspGain,ABS,Causal

def add_score_virtue_vice(df):
    """
    Adds academic score to the dataset 
    
    """
    score_r, score_c = [],[]
    for statement in df.statement : 
        clean_statement = remove_stop_word_per_statement(statement)
        s1, s2 = compute_virtue_and_vice(clean_statement)
        score_r.append(s2)
        score_c.append(s1)
    df['score_virtue']= score_r
    df['score_vice']= score_c
    return df 










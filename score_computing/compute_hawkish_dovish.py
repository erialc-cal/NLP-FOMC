#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 15:56:22 2021

@author: Claire HE

Based on Etienne Le Naour's code and this paper : https://eml.berkeley.edu/~ulrike/Papers/FOMC_48.pdf 
We add the following correction : "We drop n-grams containing more than one “goal” or “attitude” 
with different connotations.""

"""
import os
os.chdir(os.path.dirname(__file__))
from compute_scores import remove_stop_word_per_statement
from nltk.stem import WordNetLemmatizer 
from nltk import word_tokenize
lemmatizer = WordNetLemmatizer() 

liste_goal_voca =  ["inflation", "cyclical", "growth", "price", "wages", "development", "prices", "unemployment"]
list_dovish_voca = ["decrease", "slow", "weak", "low", "decreased", "decreases", "decline", "slows"]
list_hawkish_voca = ["increase", "fast", "strong", "high", "increased", "increases", "pressures", "pressure", "more"]
     
def lemmatize_statement(statement):
    """ Lemmatize statement for more effective implementation of hawkish_dovish scores """
    # Tokenize: Split the sentence into words
    lemmatized_output=""
    word_list = word_tokenize(statement)
    
    # Lemmatize list of words and join
    for w in word_list:
        lemmatized_output += lemmatizer.lemmatize(w)+' '
    return lemmatized_output

def compute_hawkish_score(statement):
    score = 0
    liste_statement = statement.split()
    nb_dovish_word = 0
    nb_hawkish_word = 0
    
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
    if nb_hawkish_word + nb_dovish_word != 0:
        score = (nb_hawkish_word - nb_dovish_word) / (nb_hawkish_word + nb_dovish_word)
    return score

def compute_FOMC_score(statement, n_gram=5):
    """ Corrected version of the hawkish score with tunable n-gram"""
    score = 0
    word_list = word_tokenize(statement)
    nb_dovish_w = 0
    nb_hawkish_w= 0
    
    for idx, word in enumerate(word_list):
        if word in liste_goal_voca :
            flag_dovish=False
            flag_hawkish=False
            for subword in word_list[int(idx-n_gram//2):int(idx+n_gram//2)]:
                if word != 'unemployment' and subword in list_dovish_voca:
                    nb_dovish_w +=1
                    flag_dovish = True
                elif word != 'unemployment' and subword in list_hawkish_voca:
                    nb_hawkish_w +=1
                    flag_hawkish = True
                elif word ==  'unemployment' and subword in list_dovish_voca:
                    nb_hawkish_w +=1
                    flag_hawkish = True
                elif  word ==  'unemployment' and subword in list_hawkish_voca:
                    nb_dovish_w +=1 
                    flag_dovish = True
                else : 
                    pass
            if flag_dovish and flag_hawkish :
                nb_dovish_w -= 1
                nb_hawkish_w -= 1
        else : 
            pass
    if nb_hawkish_w + nb_dovish_w != 0: 
        score = (nb_hawkish_w - nb_dovish_w)/(nb_hawkish_w + nb_dovish_w)
    return score

def add_hawkish_score(df, n_gram=5):
   
    """
    Adds positivity score to the dataset with n-gram choice
    
    """
    score = []
    for statement in df.statement : 
        clean_statement = remove_stop_word_per_statement(statement)
        lemma = lemmatize_statement(clean_statement)
        score.append(compute_FOMC_score(lemma, n_gram = n_gram))
    df['score_hawkish']= score
    return df 

#%% Test
df2 = pd.read_csv(parent+'/update_version_7.csv', low_memory=True)

add_hawkish_score(df2, 11)
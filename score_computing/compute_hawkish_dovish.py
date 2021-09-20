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



def compute_hawkish_score(statement):

	liste_statement = statement.split()
	nb_dovish_word = 0
	nb_hawkish_word = 0
    

	liste_goal_voca =  ["inflation", "cyclical", "growth", "price", "wages", "development", "prices", "unemployment"]
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
		if nb_hawkish_word + nb_dovish_word != 0:
			score = (nb_hawkish_word - nb_dovish_word) / (nb_hawkish_word + nb_dovish_word)
		else:
			score = 0

	return score

def add_hawkish_score(df):
   
    """
    Adds positivity score to the dataset 
    
    """
    score = []
    for statement in df.statement : 
        clean_statement = remove_stop_word_per_statement(statement)
        score.append(compute_hawkish_score(clean_statement))
    df['score_hawkish']= score
    return df 


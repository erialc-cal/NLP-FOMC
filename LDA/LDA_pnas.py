#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 15:35:24 2021

@author: Claire He
 Inspired by PNAS article

"""
import numpy as np
import pandas as pd
#%%
#### Prepare speech document : 
file_path ='/Users/h2jw/Documents/GitHub/NLP-FOMC/scrapping/df_statement_real.csv'

df = pd.read_csv(file_path, low_memory=True)
    
#%% 

#### Extra cleaning    
    
def RemoveBadCarac(mot):
    """
    remove a list of bad carac in a word
    """
    bad_carac = [",", "*", "'", "]", "[", "-", ".", "!", "?", " ", '', "(", ")", "œ", "$", "™", "š", "ﬁ"]
    mot_propre = list()
    for carac in mot:
        if carac not in bad_carac and not carac.isnumeric():
            mot_propre.append(carac)
        else:
            pass
    #return mot
    return("".join(mot_propre))


clean = []
for word in lines.lower().split():
    if len(word) < 4:
        pass
    else :
        clean.append(RemoveBadCarac(word))
        
# For 2015 07 29 there are 33348 words in the speech

#%%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 13:33:08 2021

@author: Claire He

Main script to compute all scores and add them to the dataset 

"""
### PACKAGES 
import os
dir_name = os.path.dirname(os.path.abspath(__file__)) # os.path.dirname(__file__)
os.chdir(dir_name)
from compute_scores import *
from compute_hawkish_dovish import add_hawkish_score
import time 

t1 = time.time()

### Initial dataset
file_path ='/Users/h2jw/Documents/GitHub/NLP-FOMC/scrapping/df_version5.csv'

df = pd.read_csv(file_path, low_memory=True)
print("DATASET IS LOADED")


### Add positivity score 
print("Compute positivity score")
df = add_score_positivity(df)

### Add uncertainty score
print("Compute uncertainty score")
df = add_score_incertitude(df)

### Add uncertainty score
print("Compute econo score")
df = add_score_econo(df)

### Add uncertainty score
print("Compute affirmation score")
df = add_score_affirmation(df)

### Add uncertainty score
print("Compute hostile score")
df = add_score_hostile(df)

### Add uncertainty score
print("Compute academ score")
df = add_score_academ(df)

### Add uncertainty score
print("Compute virtue and vice score")
df = add_score_virtue_vice(df)
#%%
print("Compute hawkish score")
df = add_hawkish_score(df)

#t2 = time.time()

print("Total time : ", t2-t1, "seconds")

#%% SAVING DATA

df.to_csv("final_df2015.csv")
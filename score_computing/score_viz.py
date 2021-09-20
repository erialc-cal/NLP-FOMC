#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 16:03:17 2021

@author: Claire He

Plotting scores and visuals
This file is a script not a module. 
"""
#%% Packages 
import numpy as np
import os 
project_directory = os.path.dirname(__file__)
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#%% Data

df = pd.read_csv(project_directory+'/final_df2015.csv', low_memory=True)


#%% Global visuals
x = ['econo', 'academ', 'uncertainty', 'hostility', 'positivity', 'affirmation', 'virtue', 'vice']
y = [np.mean(df.score_econo), np.mean(df.score_academ), np.mean(df.score_uncert), np.mean(df.score_hostile),np.mean(df.score_posi), np.mean(df.score_affi), np.mean(df.score_virtue), np.mean(df.score_vice)]
sns.barplot(x,y)
plt.title(f"Mean value of all scores on statements made in from {np.min(df.Date)} to {np.max(df.Date)}")

#%% Per chair visuals




#%% Per interlocutor visuals
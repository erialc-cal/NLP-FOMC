#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 11:18:20 2021

@author: h2jw
"""
import pandas as pd

topic_desc = "/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test 2/topic_description.csv"

t_desc = pd.read_csv(topic_desc)

pres = "/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test 2/president_top_topics.csv"

pres_topics = pd.read_csv(pres)

dico = '/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test 2/dict.csv'

dico_topics = pd.read_csv(dico)

dt_query = "/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test 2/dt_query.csv"

query  = pd.read_csv(dt_query)

dt = "/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test 2/dt.csv"

dt_df = pd.read_csv(dt)


df_final = pd.read_csv("/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test 2/final_output_agg.csv")
df_final = df_final.astype({ 'T0':'float64', 'T1':'float64', 'T2':'float64', 'T3':'float64', 'T4':'float64', 'T5':'float64', 'T6':'float64',
       'T7':'float64', 'T8':'float64', 'T9':'float64', 'T10':'float64', 'T11':'float64', 'T12':'float64', 'T13':'float64', 'T14':'float64', 'T15':'float64', 'T16':'float64',
       'T17':'float64', 'T18':'float64', 'T19':'float64', 'T20':'float64', 'T21':'float64', 'T22':'float64', 'T23':'float64', 'T24':'float64', 'T25':'float64', 'T26':'float64',
       'T27':'float64', 'T28':'float64', 'T29':'float64'})

df_heatmap = df_final.drop(columns='year').set_index('chair_in_charge')


#%%
from tqdm import trange
import numpy as np

l_topics = []
l_scores = []
for i in trange(1,30):
    l_topics.append(t_desc.iloc[2*i-1].tolist()[1:13])
    l_scores.append(t_desc.iloc[2*i].tolist()[1:13])
    
l_scores = [np.float_(elem) for elem in l_scores]
#%%
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(20,10))
sns.heatmap(l_scores,cmap="YlGnBu",annot=l_topics, fmt="")


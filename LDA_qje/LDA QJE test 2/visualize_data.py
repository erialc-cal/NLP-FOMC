#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 11:18:20 2021

@author: h2jw
"""
import pandas as pd

# SELECT TEST VISUALIZATION NUMBER

nb = 4



#%% 
topic_desc = f"/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test {nb}/topic_description.csv"

t_desc = pd.read_csv(topic_desc)

pres = f"/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test {nb}/president_top_topics.csv"

pres_topics = pd.read_csv(pres)

dico = f'/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test {nb}/dict.csv'

dico_topics = pd.read_csv(dico)

dt_query = f"/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test {nb}/dt_query.csv"

query  = pd.read_csv(dt_query)

dt = f"/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test {nb}/dt.csv"

dt_df = pd.read_csv(dt)

tr = f"/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test {nb}/tfidf_ranking.csv"

dt_tr = pd.read_csv(tr)


df_final = pd.read_csv(f"/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test {nb}/final_output_agg.csv")
df_final = df_final.astype({ 'T0':'float64', 'T1':'float64', 'T2':'float64', 'T3':'float64', 'T4':'float64', 'T5':'float64', 'T6':'float64',
       'T7':'float64', 'T8':'float64', 'T9':'float64', 'T10':'float64', 'T11':'float64', 'T12':'float64', 'T13':'float64', 'T14':'float64', 'T15':'float64', 'T16':'float64',
       'T17':'float64', 'T18':'float64', 'T19':'float64', 'T20':'float64', 'T21':'float64', 'T22':'float64', 'T23':'float64', 'T24':'float64', 'T25':'float64', 'T26':'float64',
       'T27':'float64', 'T28':'float64', 'T29':'float64'})

df_heatmap = df_final.drop(columns='year').set_index('chair_in_charge')


#%%
from tqdm import trange
import numpy as np


l_scores = [t_desc.iloc[0].tolist()[1:14]]
l_col0 = t_desc.columns.tolist()[1:14]
l_topics = [l_col0]
for i in trange(1,30):
    l_topics.append(t_desc.iloc[2*i-1].tolist()[1:14])
    l_scores.append(t_desc.iloc[2*i].tolist()[1:14])
    
l_scores = [np.float_(elem) for elem in l_scores]

#%% SAME VISUALS AS IN ARTICLE
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(20,10))
sns.heatmap(l_scores,cmap="Purples",annot=l_topics, fmt="")
plt.title("Topics ")
plt.show() 

#%% VISUALS PER CHAIR PER YEAR
plt.figure()
df_final2 = df_final.set_index(['chair_in_charge', 'year'])
sns.heatmap(df_final2)
plt.title("Distribution des topics par année")
plt.show()

#%% TFIDF RANK
dt_tr['score']=dt_tr['49.296371']
plt.plot(dt_tr.score)




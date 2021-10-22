#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 16:13:01 2021

@author: Claire HE

Compute procyclicality of statements
"""

import pandas as pd
import datetime as dt
from tqdm import trange

#%%
cycle = pd.read_csv("/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/Additional Data/20210719_cycle_dates_pasted.csv")

cycle = cycle.astype({'peak':'datetime64', 'trough':'datetime64'})


file_path ='/Users/h2jw/Documents/GitHub/NLP-FOMC/update_version_8.csv'
df = pd.read_csv(file_path, encoding="utf-8")

df.Date = df.Date.astype('datetime64')


#%%

# peak to trough : recession
# trough to peak : expansion
#cycle['peak']= cycle.peak.dt.year
#cycle['trough']=cycle.trough.dt.year
def procyclicality_score(df):
    procyclicality = [1 for i in range(len(df))]
    for idx in trange(len(df)):
        year = df.iloc[[idx]]['Date'][idx] 
        
        for idx2 in range(len(cycle)):
            peak, trough = cycle.iloc[[idx2]]['peak'][idx2],cycle.iloc[[idx2]]['trough'][idx2]
   
            if year <= trough and year >= peak :
                procyclicality[idx] = -1
            elif year == trough:
                procyclicality[idx]= -1
                
            else : 
                pass
    return procyclicality



#df['procyclicality']=procyclicality


#%%

def procyclicality_topics(topic_dictionary,df):
    df['procyclicality']= procyclicality_score(df)
    pro_list = []
    for idx in trange(len(df)):
        for word in topic_dictionary:
            w_procyclicality = 0
            if word in df.iloc[[idx]]['lemmatized'][idx] :
                w_procyclicality += df.iloc[[idx]]['procyclicality'][idx] 
            else:
                pass
            pro_list.append(w_procyclicality)
    return pro_list

#%%
nb = 2

topic_desc = f"/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test {nb}/topic_description.csv"

t_desc = pd.read_csv(topic_desc, names=None)

pres = f"/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test {nb}/president_top_topics.csv"

pres_topics = pd.read_csv(pres, names=None)

colnames = ['topics', 'score']
dico = f'/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test {nb}/dict.csv'

dico_topics = pd.read_csv(dico, names=colnames)

dt_query = f"/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test {nb}/dt_query.csv"

query  = pd.read_csv(dt_query, names=None)

df_dt = f"/Users/h2jw/Documents/GitHub/NLP-FOMC/LDA_qje/LDA QJE test {nb}/dt.csv"

dt_df = pd.read_csv(df_dt, names=None)


#%%


topic_dictionary = dico_topics["topics"]

pro = procyclicality_topics(topic_dictionary,df)




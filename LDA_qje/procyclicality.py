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
#df['year']=df.Date


#%%

# peak to trough : recession
# trough to peak : expansion
#cycle['peak']= cycle.peak.dt.year
#cycle['trough']=cycle.trough.dt.year

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


df['procyclicality']=procyclicality
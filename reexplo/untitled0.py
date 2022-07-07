#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 13:18:24 2022

@author: Claire He
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#%% 

clean_data = r"/Users/h2jw/Documents/GitHub/NLP-FOMC/score_computing/scrapped_cleaned.csv"
df1 = pd.read_csv(clean_data)

#%% 

full_data = r"/Users/h2jw/Documents/GitHub/NLP-FOMC/score_computing/score_df_7.csv"
df2 = pd.read_csv(full_data)

#%%

from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
import matplotlib.dates as mdates

dtFmt = mdates.DateFormatter('%Y-%b') # define the formatting
plt.gca().xaxis.set_major_formatter(dtFmt) 
# show every 12th tick on x axes
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.xticks(rotation=90, fontweight='light',  fontsize='x-small',)

df2.Date = df2.Date.astype('datetime64')

#%%

# score analysis by date

plt.plot(df2[['Date','score_posi',
       'score_uncert', 'score_econo', 'score_affi', 'score_hostile',
       'score_academ', 'score_virtue', 'score_vice', 'score_complexity',
       'score_hawkish']].groupby('Date').agg("mean"), label=['score_posi',
       'score_uncert', 'score_econo', 'score_affi', 'score_hostile',
       'score_academ', 'score_virtue', 'score_vice', 'score_complexity',
       'score_hawkish'])
plt.legend()
plt.show()


#%%

# refine by similar trends

plt.figure()
plt.plot(df2[['Date',
      'score_hostile',
       'score_academ',  'score_complexity',
       ]].groupby('Date').agg("mean"), label=[
      'score_hostile',
       'score_academ',  'score_complexity',
       ])
plt.legend()
plt.show()

plt.figure()
plt.plot(-df2[['Date', 'score_econo' ]].groupby('Date').agg("mean"), label='score econo')
plt.plot(df2[['Date', 'score_uncert']].groupby('Date').agg("mean"), label='score uncertainty')
plt.legend()
plt.show()


#%%









#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 09:59:07 2021

@author: h2jw
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

res3 = np.load('res.npy')
nov3 = np.load('nov.npy')
tran3 = np.load('tran.npy')
voc = np.load('voc.npy')
               
#%%
fig, ax = plt.subplots(1,3)
sns.distplot(nov3, ax=ax[0])
ax[0].set_title('novelty')
sns.distplot(res3, ax=ax[1])
ax[1].set_title('resonance')
sns.distplot(tran3, ax=ax[2])
ax[2].set_title('transience')


#%%

fig, ax = plt.subplots(1,3)
sns.scatterplot(voc[50:len(voc)-50],nov3, ax=ax[0])
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 15:35:24 2021

@author: Claire He
 Inspired by QJE Hansen article 

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#%%
#### Prepare speech document : 
file_path ='/Users/h2jw/Documents/GitHub/NLP-FOMC/update_version_7.csv'

df = pd.read_csv(file_path, low_memory=True)
    
#%% 


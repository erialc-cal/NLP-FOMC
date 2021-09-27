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

from gensim.parsing.preprocessing import STOPWORDS

import nltk
nltk.data.path.append('nltk_data')
from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer 


stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer() 

#%%
#### Prepare speech document : 
file_path ='/Users/h2jw/Documents/GitHub/NLP-FOMC/update_version_7.csv'

df = pd.read_csv(file_path, low_memory=True)
    
#%% 

### VOCABULARY AND MODEL SELECTION

## COLLOQUIAL TRANSFORMATION
#    " First, we identify collocations, or sequences of words that have
# a specific meaning. For example, “labor market” corresponds to a
# single economic concept but is composed of two separate words.
# To do this we first use the part-of-speech tagger described in
# Toutanova et al. (2003) to tag every word in the FOMCtranscripts.
# We then tabulate the frequencies of part-of-speech patterns identified
# in Justeson and Katz (1995) as likely to correspond to collocations.
# 16 Finally we create a single term for two-word (three-word)
# sequences whose frequency is above 100 (50). "   
def colloquial_transformation(statement):
    return 

# >>> https://nlp.stanford.edu/software/tagger.shtml POS TAGGER
    


# The second step of preprocessing is to remove common stopwords
# like “the” and “of” that appear frequently in all texts. The
# third step is to convert the remaining terms into their linguistic
# roots through stemming so that, for example, “preferences”,
# “preference,” and “prefers” all become “prefer.” The outcome of
# stemming need not be an English word. Finally, we follow the
# suggestion of Blei and Lafferty (2009) and rank the remaining
# words using term frequency-inverse document frequency (tf-idf), a
# measure of informativeness that punishes both rare and frequent
# words. Figure I plots the tf-idf values for each word; based on inspection
# we drop all terms ranked 9,000 or lower.


def stem_tfidf(statement):
    lemmatize_list=""
    final_list = list()
    intermed_list = statement.lower().split()
    for ele in intermed_list:
        if (ele not in STOPWORDS) and (ele not in stop_words) :
            final_list.append(ele)
        else:
            pass
    final_list = list(filter(None, final_list))
    for ele in final_list:
        lemmatize_list += lemmatizer.lemmatize(ele) 
    
    return lemmatize_list






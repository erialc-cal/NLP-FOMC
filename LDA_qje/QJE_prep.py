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
from tqdm import trange 
from gensim.parsing.preprocessing import STOPWORDS
import seaborn as sns
import nltk
nltk.data.path.append('nltk_data')
from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer 

from nltk.tokenize import word_tokenize

from itertools import groupby
stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer() 
import datetime as dt

#%%
#### Prepare speech document : 
file_path ='/Users/h2jw/Documents/GitHub/NLP-FOMC/update_version_7.csv'

df = pd.read_csv(file_path, low_memory=True)
df.Date = df.Date.astype('datetime64')
df1 = df[df.Date.dt.year==2015]

#%%
statement = df.statement[[230]][230]

text = word_tokenize(statement)
POS = nltk.pos_tag(text)


#%% 

### VOCABULARY AND MODEL SELECTION

## COLLOQUIAL TRANSFORMATION
#    " First, we identify collocations, or sequences of words that have
# a specific meaning. For example, “labor market” corresponds to a
# single economic concept but is composed of two separate words.
# To do this we first use the part-of-speech tagger described in
# Toutanova et al. (2003) to tag every word in the FOMCtranscripts.
# We then tabulate the frequencies of part-of-speech patterns identified
# in Justeson and Katz (1995).
# These are adjective-noun; noun-noun; adjective-adjective-noun; adjectivenoun-
# noun; noun-adjective-noun; noun-noun-noun; and noun-preposition-noun.
# Finally we create a single term for two-word (three-word) as likely to correspond to collocations.
# sequences whose frequency is above 100 (50). "   



# We try to reproduce this work but we don't use Toutanova's work since it 
# runs on Java but with the nltk POS tagger 
# Original can be found here :
# >>> https://nlp.stanford.edu/software/tagger.shtml POS TAGGER
    

def colloquial_transformation(statement):
    
    """ NLTK POS TAGGER : 
        find the list of abbreviations here : https://medium.com/@muddaprince456/categorizing-and-pos-tagging-with-nltk-python-28f2bc9312c3
        
        Js = JJR or JJR or JJS
        Ns = NN or NNP or NNS or NNPS 
        
        Colloquial combinations according to Justeson and Katz (1995) :
            - Js+Ns
            - Js*2+Ns
            - Ns*2
            - Js+Ns*2
            - Ns+Js+Ns
            - Ns*3
            - Ns+IN+Ns
            
        Returns list of colloquials
    """
    
    text = word_tokenize(statement)
    POS = nltk.pos_tag(text)
    colloquial=[]
    pos_list=[]
    for i, pos in enumerate(POS[1:len(POS)-1]):
        word, tag = pos
        bw, btag = POS[i-1]
        try:
            aw, atag = POS[i+1]
        except:
            pass
       
        if ('NN' in tag) and ('NN' in atag) and ('NN' in btag):
            colloquial.append(bw+' '+word+' '+aw)
            pos_list.append(pos)
        elif ('JJ' in btag) and ('NN' in tag) and ('JJ' in atag):
            colloquial.append(bw+' '+word+' '+aw)
            pos_list.append(pos)
        elif ('NN' in btag) and ('JJ' in tag) and ('NN' in atag):
            colloquial.append(bw+' '+word+' '+aw)
            pos_list.append(pos)
        elif ('JJ' in btag) and ('JJ' in tag) and ('NN' in atag):
            colloquial.append(bw+' '+word+' '+aw)
            pos_list.append(pos)
        elif ('NN' in btag) and ('IN' in tag) and ('NN' in atag):
            colloquial.append(bw+' '+word+' '+aw)
            pos_list.append(pos)
        elif ('NN' in tag) and ('NN' in atag) :
            colloquial.append(word+' '+aw)
            pos_list.append(pos)
        elif ('JJ' in tag) and ('NN' in atag) :
            colloquial.append(word+' '+aw)
            pos_list.append(pos)
        else :
            pass
    return colloquial, pos_list


def get_freq_two_three(statement):
    """ Gets the colloquials whose frequency are above 100 """
    final_col, final_pos = [],[]
    col_list, pos_list =colloquial_transformation(statement)
    freq = [len(list(group)) for key, group in groupby(col_list)]
    for idx in range(len(freq)):
        if freq[idx] >= 100:
            final_col.append(col_list[idx])
            final_pos.append(pos_list[idx])
        else : 
            pass
    return final_col, final_pos


def plot_freq_colloquial(list_statement):
    """ Plots colloquial sentences' frequency distributions """
    # Concaténer tous les statements
    statement = ""
    for s in list_statement:
        statement += " "+s
    col_list, pos_list = colloquial_transformation(statement)
    freq = [len(list(group)) for key, group in groupby(col_list)]
    fig = plt.figure()
    plt.title("Colloquial frequency distribution")
    plt.hist(freq)
    plt.plot()

def replace_words_by_colloquials(statement):
    """ Replaces in statement the individual words by colloquial sentences """
    text = word_tokenize(statement)
    new_text=""
    col, pos = get_freq_two_three(statement)
    for idx, word in enumerate(text):
        if (idx in pos) :
            ind = pos.index(idx)# two-words colloquial
            if len(col[ind].split())==2:
                new_text+=" "+col[ind]
            elif len(col[ind].split())==3: #three-words colloquial
                new_text+= " "+col[ind]
        else :
            new_text+= " "+word
    return new_text 
                    
            
    
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
        lemmatize_list += " "+lemmatizer.lemmatize(ele) 
    
    return lemmatize_list




#%%
df1 = df1.reset_index()

clean=[]
for i in trange(len(df1.statement)):
    statement = df1.statement.iloc[[i]][i]
    statement = stem_tfidf(statement)
    clean_statement = replace_words_by_colloquials(statement)
    clean.append(clean_statement)
    
df1['cleaned']=clean
#%%


df1[['cleaned','chair_in_charge', 'Date']].to_csv('clean_statements.csv')


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 13:41:22 2021

@author: Claire He 

LDA on a corpus and measuring each chair's proximity to a topic.
Topic viz can be plotted with Topic_ext_LDA_and_cie.py.
"""

import os
project_directory = os.path.dirname(__file__)
from time import time
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt

#%%
#### PARAMETERS TO BE MODIFIED #####
saveFlag = True
run_script = True 
#if run_script is set to True, import data in the following lines
if run_script:
    #preprocessing
    from nltk.corpus import stopwords
    stop = stopwords.words('english')
    stop.extend(['mr','re', 's', 'it', 'ex', 'in', 'he', 'and', 'there', 'however', 'to', 'now', 'to', 'of', 'the', 
                 'they', 'but', 'soon', 'film', 'that', 'who', 'of', 'oh','youre','like','dont', 'yes', 'thats', 'im', 'think', 'thank'])
    
    df = pd.read_csv("/Users/h2jw/Documents/GitHub/NLP-FOMC/RA_project/final_df_v4.csv", low_memory=True)
    df.statement = df.statement.fillna('')
    df = df.drop(columns = ['Unnamed: 0','Unnamed: 0.1','Unnamed: 0.1.1','Unnamed: 0.1.1.1' ])
    df['statement'] = df['statement'].str.replace('[^\w\s]','') # remove punctuation
    df["statement"] = df["statement"].str.lower().str.split() # get words with lowercase 
    df['statement'] = df['statement'].apply(lambda x: [item for item in x if item not in stop]) # remove stopwords
    df.statement = df.statement.astype('string')
    df['statement'] = df['statement'].str.replace('[^\w\s]','')
    #set data
    data = df.statement.dropna().to_list()


n_samples = len(df)
n_features = 1000
n_components = 5
n_top_words = 10
####################################

#%%
def LDA_topics(data, n_samples, n_components, n_features, n_top_words):
        # Use tf (raw term count) features for LDA.
    data_samples = data[:n_samples]   
    print("Extracting tf features for LDA...")
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                    max_features=n_features,
                                    stop_words='english')
    t0 = time()
    tf = tf_vectorizer.fit_transform(data_samples)
    print("done in %0.3fs." % (time() - t0))
    print()

    
    print('\n' * 2, "Fitting LDA models with tf features, "
          "n_samples=%d and n_features=%d..."
          % (n_samples, n_features))
    lda = LatentDirichletAllocation(n_components=n_components, max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    t0 = time()
    doc_topic = lda.fit_transform(tf)
    print("done in %0.3fs." % (time() - t0))
    
    tf_feature_names = tf_vectorizer.get_feature_names()

    top_features, weights =[], []
    for topic_idx, topic in enumerate(lda.components_):
        top_features_ind = topic.argsort()[:-n_top_words-1:-1]
        top_features.append([tf_feature_names[i] for i in top_features_ind])
        weights.append(topic[top_features_ind])
    return doc_topic, top_features, weights

#%% ######### MODELING AND SAVING DATA

if run_script:
    doc_topic, top_features, weights = LDA_topics(data, n_samples, n_components, n_features, n_top_words)


if saveFlag :
    top_f,w = [],[]
    for features in top_features:
        for words in features :
            top_f.append(words)
    for topic in weights :
        for weight in topic:
            w.append(weight)
        
    df_topics = pd.DataFrame()
    df_topics['features']=top_f
    df_topics['weights']=w
    df_topics['topic']= np.repeat([i+1 for i in range(n_components)], n_top_words)
    df_topics.to_csv(f'df_{n_components}_topics_{n_top_words}_topwords.csv')
    
    
#%% ######### CHAIR ANALYSIS WITH LDA TOPICS

# topic appearance ratio for all statements of a chair

def plot_topic_per_chair(data, all_topic, topic, chair, verbose=False):
    #sélection de la chair
    mask = data[data.chair_in_charge==chair].index
    select_topic = all_topic[mask]
    if verbose : 
        a, b = len(topic)//5, len(topic)%5
        fig, axes = plt.subplots(a, 5, figsize=(20, 8), sharex=True)
        axes = axes.flatten()
        for i in range(len(topic)):
            ax = axes[i]
            ax.barh(topic[i], select_topic[i], height=0.7)
            ax.set_title(f'Topic {i +1}',
                         fontdict={'fontsize': 30})
            ax.invert_yaxis()
            ax.tick_params(axis='both', which='major', labelsize=20)
            for i in 'top right left'.split():
                ax.spines[i].set_visible(False)
            fig.suptitle(f"Top 10 topics for the {chair}", fontsize=40)
    return select_topic
 
    

#%%

# df_per_chair['chair_in_charge']= np.repeat(chair, len(topic))
# df_per_chair['topic']= np.tile([i for i in range(len(topic))], len(chair))
# df_per_chair['ratio']=ratio1       


#%%
for chair in pd.unique(df.chair_in_charge):
    plot_topic_per_chair(df, doc_topic, top_features, chair, verbose=True)









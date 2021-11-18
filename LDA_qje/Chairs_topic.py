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
    
    df = pd.read_csv("/Users/h2jw/Documents/GitHub/NLP-FOMC/lem_clean_version_8.csv", low_memory=True)
    df.statement = df.statement.fillna('')
    df = df.drop(columns = ['Unnamed: 0']) #,'Unnamed: 0.1','Unnamed: 0.1.1','Unnamed: 0.1.1.1' ])
    df['statement'] = df['statement'].str.replace('[^\w\s]','') # remove punctuation
    df["statement"] = df["statement"].str.lower().str.split() # get words with lowercase 
    df['statement'] = df['statement'].apply(lambda x: [item for item in x if item not in stop]) # remove stopwords
    df.statement = df.statement.astype('string')
    df['statement'] = df['statement'].str.replace('[^\w\s]','')
    #set data
    data = df.statement.dropna().to_list()
    
    
#%%

n_samples = len(df)
n_features = 3000
n_components = 30
n_top_words = 100
####################################

#%% ### CORPUS ANALYSIS 


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


    
import seaborn as sns
#show 12 most used words

def plot_heatmap_corpus(weights, top_features):
    trunc_weights = []
    for elem in weights:
        trunc_weights.append(elem[:12])
        
    trunc_labels=[]
    for elem in top_features:
        trunc_labels.append(elem[:12])
        
    plt.figure(figsize=(20,12))
    sns.heatmap(trunc_weights, annot=trunc_labels, fmt='',cmap='Blues')
    plt.title('LDA sur les transcripts de 1976 à 2015, toutes chairs confondues \n 30 topics, 100 mots clés, corpus de 156 082 mots')
    plt.show()
    

#%% ######### MODELING AND SAVING DATA

if run_script:
    doc_topic, top_features, weights = LDA_topics(data, n_samples, n_components, n_features, n_top_words)

#%%
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

def plot_topic_per_chair(data, all_topic, topic, chair, verbose=False, n_components=5, n_top_words=10):
    #sélection de la chair
    mask = data[data.chair_in_charge==chair].index
    select_topic = all_topic[mask]
    top_features_ind = select_topic.argsort()[:-n_top_words - 1:-1]
   # weights = select_topic[top_features_ind]

    print(select_topic,top_features_ind, np.sum(select_topic, axis=0))
    if verbose : 
        a = len(topic)//5
        fig, axes = plt.subplots(len(topic), figsize=(20, 8), sharex=True)
        axes = axes.flatten()
        for i in range(len(topic)):
            ax = axes[i]
            ax.barh(topic[i], select_topic[topic[i]], height=0.7)
            ax.set_title(f'Topic {i +1}',
                         fontdict={'fontsize': 30})
            ax.invert_yaxis()
            ax.tick_params(axis='both', which='major', labelsize=20)
            for i in 'top right left'.split():
                ax.spines[i].set_visible(False)
            fig.suptitle(f"Top 10 topics for the {chair}", fontsize=40)
    return select_topic
 
def plot_topic_ratio(data, all_topic, topic, n_components=5, n_top_words=10):
    count_topic = []
    topic_num = [i for i in range(n_components)]
    chair_l = pd.unique(data.chair_in_charge)
    for chair in chair_l:
        mask = data[data.chair_in_charge==chair].index
        select_topic = all_topic[mask]
        count_topic.append(np.mean(select_topic, axis=0))
    #print(count_topic)
    fig, ax = plt.subplots(1, len(chair_l),figsize=(20,5))
    for i in range(len(chair_l)):
        ax[i].bar(topic_num, count_topic[i])
        ax[i].set_xlabel('Topic no.')
        ax[i].set_title(f'{chair_l[i]}')
    plt.show()


## GET INFO PER CHAIR
def plot_heatmap_chair(df, n_components, n_features, n_top_words):
    chairs = pd.unique(df.chair_in_charge)
    for chair in chairs:
        data= df[df.chair_in_charge==chair].statement.dropna().to_list()
        doc_topic, top_features, weights = LDA_topics(data, len(data),n_components, n_features, n_top_words)
        
        # if saveFlag :
        #     top_f,w = [],[]
        #     for features in top_features:
        #         for words in features :
        #             top_f.append(words)
        #     for topic in weights :
        #         for weight in topic:
        #             w.append(weight)
                
        #     df_topics = pd.DataFrame()
        #     df_topics['features']=top_f
        #     df_topics['weights']=w
        #     df_topics['topic']= np.repeat([i+1 for i in range(n_components)], n_top_words)
        #     df_topics.to_csv(f'df_{n_components}_{n_top_words}_{chair}.csv')
            
        trunc_weights = []
        for elem in weights:
            trunc_weights.append(elem[:12])
            
        trunc_labels=[]
        for elem in top_features:
            trunc_labels.append(elem[:12])
            
        plt.figure(figsize=(20,12))
        sns.heatmap(trunc_weights, annot=trunc_labels, fmt='',cmap='Blues')
        plt.title(f'LDA sur les transcripts de 1976 à 2015, {chair} \n 30 topics, 100 mots clés')
        plt.savefig(f'{chair}_30_100.png')
        plt.show()


    
#%% # GET SPEAKER SCORE PER TOPIC

def speaker_score_per_topic(df,top_features, weights):
    df.lemmatized = df.lemmatized.astype(str)
    
    df_speaker = df.groupby('interlocutor_name').apply(lambda s: ' '.join(s['lemmatized']))
    
    
    l_score = []
    l_score_f = []
    for state in df_speaker:
        for word in state.split():
            score_state = 0
            for idx in range(30):
                if word in top_features[idx]:
                    idx2 = np.where(word in top_features[idx])
                    score_state += weights[idx][idx2][0]
                
                   # print(score_state)
                else :
                    pass
            l_score.append(score_state)
        l_score_f.append(score_state)
    
    return l_score_f
# score_state = 0
# l_score = [] 
# for word in speaker0.split():
#     for idx in range(30):
#         if word in top_features[idx]:
#             idx2 = np.where(word in top_features[idx])
#             score_state += weights[idx][idx2][0]
#            # print(score_state)
#         else :
#             pass
# l_score.append(score_state)


# TEST 
df = df[df.chair_in_charge == 'CHAIRMAN GREENSPAN']
doc_topic, top_features, weights = LDA_topics(df.statement.dropna().to_list(), len(df), n_components, n_features, n_top_words)
l_score_f = speaker_score_per_topic(df, top_features, weights)

#%%

plot_topic_ratio(df, doc_topic, top_features)
plot_topic_per_chair(df, doc_topic, top_features)

# df_per_chair['chair_in_charge']= np.repeat(chair, len(topic))
# df_per_chair['topic']= np.tile([i for i in range(len(topic))], len(chair))
# df_per_chair['ratio']=ratio1       

        # top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
        # top_features = [feature_names[i] for i in top_features_ind]
        # weights = topic[top_features_ind]
# for chair in pd.unique(df.chair_in_charge):
#     select_topic= plot_topic_per_chair(df, doc_topic, top_features, chair, verbose=True)

#%%

#%%


#%% 

df = 

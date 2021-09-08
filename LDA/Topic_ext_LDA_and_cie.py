#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 12:28:04 2021

@author: Claire HE

Script file : comparing topics modelling with three methods : LDA, NMF with Frobenius norm and with Kullback Leibler divergence. 
Full statements are used in dictionary for modelling. 
Code is inspired from the following scikit-learn documentation : https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-plot-topics-extraction-with-nmf-lda-py 
"""

from time import time
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

#%%

############ DATA PREPROCESSING ###################

#nltk.download('stopwords')
from nltk.corpus import stopwords
stop = stopwords.words('english')
stop.extend(['mr','re', 's', 'it', 'ex', 'in', 'he', 'and', 'there', 'however', 'to', 'now', 'to', 'of', 'the', 
             'they', 'but', 'soon', 'film', 'that', 'who', 'of', 'oh','youre','like','dont', 'yes', 'thats', 'im', 'think', 'thank'])


df = pd.read_csv("/Users/h2jw/Documents/GitHub/NLP-FOMC/RA_project/final_df_v4.csv", low_memory=True)

df.statement = df.statement.fillna('')
df['statement'] = df['statement'].str.replace('[^\w\s]','') # remove punctuation

df["statement"] = df["statement"].str.lower().str.split() # get words with lowercase 

df['statement'] = df['statement'].apply(lambda x: [item for item in x if item not in stop]) # remove stopwords
df.statement = df.statement.astype('string')
df['statement'] = df['statement'].str.replace('[^\w\s]','')

n_samples = len(df.statement) #2000
n_features = 1000
n_components = 10
n_top_words = 10


# Load the 20 newsgroups dataset and vectorize it. We use a few heuristics
# to filter out useless terms early on: the posts are stripped of headers,
# footers and quoted replies, and common English words, words occurring in
# only one document or in at least 95% of the documents are removed.
# from sklearn.datasets import fetch_20newsgroups
# print("Loading dataset...")
# t0 = time()
# data, _ = fetch_20newsgroups(shuffle=True, random_state=1,
#                              remove=('headers', 'footers', 'quotes'),
#                              return_X_y=True)
# data_samples = data[:n_samples]
# print("done in %0.3fs." % (time() - t0))

data = df.statement.dropna().to_list()
data_samples = data[:n_samples]
#%% 


############### ANALYSIS #################@
def plot_top_words(model, feature_names, n_top_words, title):
    a, b = n_components//5, n_components%5
    fig, axes = plt.subplots(a, 5, figsize=(20, 8), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]

        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f'Topic {topic_idx +1}',
                     fontdict={'fontsize': 30})
        ax.invert_yaxis()
        ax.tick_params(axis='both', which='major', labelsize=20)
        for i in 'top right left'.split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=40)

    keywords = ['frobenius', 'kl','lda']
    for word in title.lower().split():
        if word in keywords:
        
            plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
            plt.savefig(f'{word}_{n_components}.png')
            plt.show()




# Use tf-idf features for NMF.
print("Extracting tf-idf features for NMF...")
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                   max_features=n_features,
                                   stop_words='english')
t0 = time()
tfidf = tfidf_vectorizer.fit_transform(data_samples)
print("done in %0.3fs." % (time() - t0))

# Use tf (raw term count) features for LDA.
print("Extracting tf features for LDA...")
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                max_features=n_features,
                                stop_words='english')
t0 = time()
tf = tf_vectorizer.fit_transform(data_samples)
print("done in %0.3fs." % (time() - t0))
print()

# Fit the NMF model
print("Fitting the NMF model (Frobenius norm) with tf-idf features, "
      "n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
t0 = time()
nmf = NMF(n_components=n_components, random_state=1,
          alpha=.1, l1_ratio=.5).fit(tfidf)
print("done in %0.3fs." % (time() - t0))


tfidf_feature_names = tfidf_vectorizer.get_feature_names()
plot_top_words(nmf, tfidf_feature_names, n_top_words,
               'Topics in NMF model Frobenius norm' )

# Fit the NMF model
print('\n' * 2, "Fitting the NMF model (generalized Kullback-Leibler "
      "divergence) with tf-idf features, n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
t0 = time()
nmf = NMF(n_components=n_components, random_state=1,
          beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,
          l1_ratio=.5).fit(tfidf)
print("done in %0.3fs." % (time() - t0))

tfidf_feature_names = tfidf_vectorizer.get_feature_names()
plot_top_words(nmf, tfidf_feature_names, n_top_words,
               'Topics in NMF model generalized KL divergence')


print('\n' * 2, "Fitting LDA models with tf features, "
      "n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
lda = LatentDirichletAllocation(n_components=n_components, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
t0 = time()
lda.fit(tf)
print("done in %0.3fs." % (time() - t0))

tf_feature_names = tf_vectorizer.get_feature_names()
plot_top_words(lda, tf_feature_names, n_top_words, 'Topics in LDA model')




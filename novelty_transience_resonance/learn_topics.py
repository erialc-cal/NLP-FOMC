# coding: utf-8
"""
Example code for producing topic mixtures, given a file of text data.

Author: Alexander T. J. Barron
Modified by: Claire He 
Date Created: 2017-11-25

"""

# import argparse
import os
import pandas as pd
project_directory ,_ = os.path.split(os.path.dirname(__file__))

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from lda import LDA



def learn_topics(topicnum, df_flag=False,dirpath=project_directory+'/novelty_transience_resonance/text.txt', df=''):
    texts = ''
    if df_flag :
       # print("dirpath should be dataframe path")
        for statement in df.statement :
            texts += statement
        with open(project_directory+'/temporary_text.txt', 'w') as sortie:
            sortie.write(texts)
            sortie.close
        with open(project_directory+'/temporary_text.txt') as f:
            texts = f.readlines()
    else :
        with open(dirpath) as f:
            texts = f.readlines()
        
    # Get vocabulary and word counts.  Use the top 10,000 most frequent
    # lowercase unigrams with at least 3 alphabetical, non-numeric characters,
    # punctuation treated as separators.
    CVzer = CountVectorizer(token_pattern=r"(?u)\b[^\W\d]{3,}\b",
                            max_features=None,
                            lowercase=True)
    doc_vcnts = CVzer.fit_transform(texts)
    vocabulary = CVzer.get_feature_names()

    # Learn topics.  Refresh conrols print frequency.
    lda_model = LDA(topicnum, n_iter=8000, refresh=2000) 
    doc_topic = lda_model.fit_transform(doc_vcnts)
    topic_word = lda_model.topic_word_

    os.remove(project_directory+'/temporary_text.txt')
    return doc_topic, topic_word, vocabulary

def save_topicmodel(doc_topic, topic_word, vocabulary, dirpath):

    ## Topic mixtures.
    topicmixture_outpath = os.path.join(dirpath, "topic_mixtures.txt")
    np.savetxt(topicmixture_outpath, doc_topic)

    ## Topics.
    topic_outpath = os.path.join(dirpath, "topics.txt")
    np.savetxt(topic_outpath, topic_word)

    ## Vocabulary order.
    vocab_outpath = os.path.join(dirpath, "vocabulary.txt")
    with open(vocab_outpath, mode="w") as f:
        for v in vocabulary:
            f.write(v + "\n")

    return topicmixture_outpath, topic_outpath, vocab_outpath

# def main(topicnum, dirpath):

#     doc_topic, topic_word, vocabulary = learn_topics(topicnum)

#     topicmixture_outpath, topic_outpath, vocab_outpath = \
#             save_topicmodel(doc_topic, topic_word, vocabulary, dirpath)


###  Tests : 
# doc_topic, topic_word, vocabulary = learn_topics(100)

# topicmixture_outpath, topic_outpath, vocab_outpath = \
#         save_topicmodel(doc_topic, topic_word, vocabulary, project_directory+'/novelty_transience_resonance/')


#%%
# if __name__ == "__main__":

#     parser = argparse.ArgumentParser()
#     parser.add_argument("topicnum", type=int,
#             help="Desired number of topics.")
#     parser.add_argument("dirpath", type=str,
#             help="Directory path to enclose results.") 
#     args = parser.parse_args()

#     main(args.topicnum, args.dirpath)

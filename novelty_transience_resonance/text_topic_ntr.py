# coding: utf-8
"""
Script executing topic modeling and calculation of novelty, transience, and
resonance in succession.

Author: Alexander T. J. Barron
Date Created: 2017-11-25

"""

# import argparse
import os
project_directory = os.path.dirname(__file__)
parent, _ = os.path.split(project_directory)
import numpy as np
import pandas as pd
from learn_topics import learn_topics, save_topicmodel
from calculate_novelty_transience_resonance import \
        novelty_transience_resonance, save_novel_trans_reson
        
        
file_path ='/Users/h2jw/Documents/GitHub/NLP-FOMC/update_version_7.csv'

df = pd.read_csv(file_path, low_memory=True)       

#%% 
def main(topicnum, scale, dirpath):

    doc_topic, topic_word, vocabulary = learn_topics(topicnum)

    topicmixture_outpath, topic_outpath, vocab_outpath = \
            save_topicmodel(doc_topic, topic_word, vocabulary, dirpath)

    novelties, transiences, resonances = \
            novelty_transience_resonance(doc_topic, scale)
    
    return novelties, transiences, resonances
    #save_novel_trans_reson(novelties, transiences, resonances, dirpath)
    
#%%
# We coarse-grain into 100 topics 
topicnum = 100
scale = 20
with open("/Users/h2jw/Documents/GitHub/NLP-FOMC/novelty_transience_resonance/2012-2015/topics.txt", 'r') as f:
    doc_topic = f.readlines()
with open("/Users/h2jw/Documents/GitHub/NLP-FOMC/novelty_transience_resonance/2012-2015/topic_mixtures.txt", 'r') as f:
    topic_word = f.readlines()
with open("/Users/h2jw/Documents/GitHub/NLP-FOMC/novelty_transience_resonance/2012-2015/vocabulary.txt", "r") as f:
    vocabulary = f.readlines()
  

doc_topic = np.float_(doc_topic[0].split())
topic_word = topic_word[0].split()

#%%
topic_w = np.zeros((topicnum, len(vocabulary)))
for i in range(len(topic_word)):
    topic_w[i,:]=topic_word[i].split()


#%%

def prepare_ntr(df, two_chairs=False, chair_in_charge=['CHAIR YELLEN']):
    if two_chairs : 
        # comparing novelty, transience and resonance of topics from two different successive chairs
        assert len(chair_in_charge)==2
        mask = (df.chair_in_charge.isin(chair_in_charge))
        print("Document preparation and topic processing...")
        doc_topic, topic_word, vocabulary = learn_topics(100, df_flag=True, df=df[mask])
        # print("Topic processing...")
        # topicmixture_outpath, topic_outpath, vocab_outpath = \
        #     save_topicmodel(doc_topic, topic_word, vocabulary, project_directory+f'/between_chairs/{chair_in_charge[0]}_{chair_in_charge[1]}_')
        print("Computing novelty, transience and resonance...")
        novelties, transiences, resonances = \
            novelty_transience_resonance(doc_topic, scale)
    else :
        assert len(chair_in_charge)==1
        print("Document preparation...")
        mask = df.chair_in_charge.isin(chair_in_charge)
        print('Topic processing...')
        doc_topic, topic_word, vocabulary = learn_topics(100, df_flag=True, df=df[mask])
        # topicmixture_outpath, topic_outpath, vocab_outpath = \
        #     save_topicmodel(doc_topic, topic_word, vocabulary, project_directory+f'/per_chair/{chair_in_charge[0]}_')
        print('Computing novelty, transience and resonance...')
        novelties, transiences, resonances = \
            novelty_transience_resonance(doc_topic, scale)
        
    return novelties, transiences, resonances
    #%% TESTS
    

novelties, transiences, resonances = novelty_transience_resonance(topic_w.T, 100)

#novelties, transiences, resonances = prepare_ntr(df1, two_chairs=False, chair_in_charge=['CHAIR YELLEN'])
    
    
    #%%
    
def create_text():
    # Text and vocabulary preparation
    texts = ""
    for filename in os.listdir(parent+'/scrapping/transcript_to_word_set/'):
        try :
            with open(parent+'/scrapping/transcript_to_word_set/'+filename, 'r') as doc:
                texts += doc.read()
        except : 
            pass
    with open(project_directory+'/text.txt', 'w') as sortie:
        sortie.write(texts)
        sortie.close
        
#%%

# if __name__ == "__main__":

#     parser = argparse.ArgumentParser()
#     # parser.add_argument("textpath", type=str,
#     #        help="Path to file of text data, one document per row, " \
#     #                "rows delimited with newlines.") 
#     parser.add_argument("topicnum", type=int,
#             help="Desired number of topics.")
#     parser.add_argument("scale", type=int,
#             help="Size of windows for calculation.")
#     parser.add_argument("dirpath", type=str,
#            help="Directory path to enclose results.") 
#     args = parser.parse_args()

#     main(args.topicnum, args.scale, args.dirpath)

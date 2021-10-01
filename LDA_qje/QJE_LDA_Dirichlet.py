#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 14:51:50 2021

@author: Claire HE
inspired by Hansen (2017) article "Transparency and Deliberation in the FOMC"

"""
import pandas as pd
import topicmodels


#### Prepare speech document : 
file_path ='/Users/h2jw/Documents/GitHub/NLP-FOMC/update_version_7.csv'
data = pd.read_csv(file_path, encoding="utf-8")
#data = data[data.year >= 1947]
data.Date = data.Date.astype('datetime64')
data['year']=data.Date.dt.year

#%%


docsobj = topicmodels.RawDocs(data.statement, "long")
docsobj.token_clean(1)
docsobj.stopword_remove("tokens")
docsobj.stem()
docsobj.stopword_remove("stems")
docsobj.term_rank("stems")
docsobj.rank_remove("tfidf", "stems", docsobj.tfidf_ranking[5000][1])

all_stems = [s for d in docsobj.stems for s in d]
print("number of unique stems = %d" % len(set(all_stems)))
print("number of total stems = %d" % len(all_stems))


#%%

###############
# estimate topic model
###############

ldaobj = topicmodels.LDA.LDAGibbs(docsobj.stems, 30)

ldaobj.sample(0, 50, 10)
ldaobj.sample(0, 50, 10)

ldaobj.samples_keep(4)
ldaobj.topic_content(20)

dt = ldaobj.dt_avg()
tt = ldaobj.tt_avg()
ldaobj.dict_print()

# data = data.drop('statement', 1)
# for i in xrange(ldaobj.K):
#     data['T' + str(i)] = dt[:, i]
# data.to_csv("final_output.csv", index=False)

###############
# query aggregate documents
###############

data['statement'] = [' '.join(s) for s in docsobj.stems]
aggspeeches = data.groupby(['year', 'chair_in_charge'])['statement'].\
    apply(lambda x: ' '.join(x))
aggdocs = topicmodels.RawDocs(aggspeeches)

queryobj = topicmodels.LDA.QueryGibbs(aggdocs.tokens, ldaobj.token_key,
                                      ldaobj.tt)
queryobj.query(10)
queryobj.perplexity()
queryobj.query(30)
queryobj.perplexity()

dt_query = queryobj.dt_avg()
aggdata = pd.DataFrame(dt_query, index=aggspeeches.index,
                       columns=['T' + str(i) for i in range(queryobj.K)])
aggdata.to_csv("final_output_agg.csv")

###############
# top topics
###############


def top_topics(x):
    top = x.values.argsort()[-5:][::-1]
    return(pd.Series(top, index=range(1, 6)))

temp = aggdata.reset_index()
ranking = temp.set_index('chair_in_charge')
ranking = ranking - ranking.mean()
ranking = ranking.groupby(level='chair_in_charge').mean()
ranking = ranking.sort_values('year')
ranking = ranking.drop('year', 1)
ranking = ranking.apply(top_topics, axis=1)
ranking.to_csv("president_top_topics.csv")
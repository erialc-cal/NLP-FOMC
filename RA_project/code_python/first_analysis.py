

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation



n_features = 20
n_components = 10
n_top_words = 5

project_directory = '/Users/etiennelenaour/Desktop/Stage/'
l_month = ['January','February','March','April','May','June','July','August','September','October','November','December']
l_dates = list()


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()


with open ('/Users/etiennelenaour/Desktop/Stage/csv_files/dates_fomc.csv', 'r') as doc :
    head = doc.readline()
    dates = doc.readlines()
    dates_to_chg = []
    for line in dates :
        if line.split(',')[1] == ' Y' :
            dates_to_chg += [line.split(';')[0]]
            date = 0
            m = 1   
            for month in l_month :
                if month[:3] == line.split(';')[0].split('/')[0] :
                    date += 100 * m
                m += 1
            date += int(line.split(',')[0].split('/')[2])*10000
            date += int(line.split(',')[0].split('/')[1])
            l_dates.append(date)
            



corpus = list()

for date in l_dates[100:200]: #19870707 and 19991221

    with open(project_directory+'transcript_to_word_set/'+str(date)+'meeting.txt', 'r') as doc:
        file = doc.readlines()[0]
        corpus.append(file)


tf_vectorizer = CountVectorizer(max_df=0.70, min_df=0.01,
                                    max_features=2000,
                                    stop_words='english')

tf = tf_vectorizer.fit_transform(corpus)
#print(tf.toarray().shape)
#print(tf_vectorizer.get_feature_names())



lda = LatentDirichletAllocation(n_components=n_components, max_iter=50,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)

lda.fit(tf)

print("\nTopics in LDA model:")
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)




#print(len(corpus))




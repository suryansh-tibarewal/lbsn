import gensim
import numpy as np
f = open('interests_list.txt', 'r')
content = f.read()
interests_list = list()
for interest in content.split(','):
    interest = interest.strip()
    interest = interest.replace(" ", "_")
    interests_list.append(interest)
#print interests_list
f.close()


def galatList(interests_list):
        model = gensim.models.Word2Vec.load_word2vec_format('word2vec_models/GoogleNews-vectors-negative300.bin', binary=True)
        for interest in interests_list:
            try:
                k = model[interest]
            except KeyError:
                print interest
        

#galatList(interests_list)
#exit(1)
model = gensim.models.Word2Vec.load_word2vec_format('word2vec_models/GoogleNews-vectors-negative300.bin', binary=True)
X = np.array([0]*300)

for interest in interests_list:
    X = np.vstack([X, model[interest]])

X = np.delete(X, 0, 0)

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
print kmeans.predict([model['cricket'], model['chess'], model['painting']])
import gensim
import numpy as np

def getInterestList(fileName):
    f = open(fileName, 'r')
    content = f.read()
    interests_list = list()
    for interest in content.split(','):
        interest = interest.strip()
        interest = interest.replace(" ", "_")
        interests_list.append(interest)
    #print interests_list
    f.close()
    interests_list.sort()
    return interests_list

def main():
    model = gensim.models.Word2Vec.load_word2vec_format('word2vec_models/GoogleNews-vectors-negative300.bin', binary=True)
    interestList = getInterestList('interests_list.txt')
    print len(interestList)

    dimensions = (len(interestList), len(interestList))
    matrix = np.zeros(dimensions)
    for i in range(len(interestList)):
        for j in range(len(interestList)):
            matrix[i, j] = model.similarity(interestList[i], interestList[j])
    print type(matrix)
    print matrix.shape 

    np.savetxt('similarityMatrix.txt', matrix)
    

#main()
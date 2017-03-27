import numpy as np
from similarityMatrixGenerator import getInterestList
from math import sqrt
import pickle
from math import isnan
from constants import GOWALLA_DATASET, BRIGHTKITE_DATASET

def getSimilarityMatrix(fileName):
    return np.loadtxt(fileName)

def getIndex(interest, interestList):
    if interest not in interestList:
        print interest + ' is not present in the list.\n'
        exit(1)

    ans = -1
    for i in range(len(interestList)):
        if interest is interestList[i]:
            ans = i

    return ans

def vectorize(customList, interestList):
    X = np.zeros(len(interestList))

    for interest in customList:
        i = interestList.index(interest)
        X[i] = 1.0

    return X

def summation(v1, v2, s):
    sum = 0
    for i in range(len(v1)):
        for j in range(len(v2)):
            if (s[i,j]<=0):
                s[i,j] = 0
            sum += s[i, j]*v1[i]*v2[j]

    return sum

def soft_cosine(v1, v2, s):
    if type(s).__module__ != np.__name__:
        print 'Matrix is not a numpy array.\n'
        exit(3)
    if(len(v1) != len(v2)):
        print 'Length to 2 vectors should be same.\n'
        exit(2)

    num = summation(v1, v2, s)
    den1 = sqrt(summation(v1, v1, s))
    den2 = sqrt(summation(v2, v2, s))

    res = num/(den1*den2)
    return res

matrix = getSimilarityMatrix('similarityMatrix.txt')
interestList = getInterestList('interests_list.txt')

def get_soft_cosine2(v1, v2):
    global matrix, interestList
    X = vectorize(v1, interestList)
    Y = vectorize(v2, interestList)
    return soft_cosine(X, Y, matrix)

def getPickleDic(boolDataset):
    if boolDataset == GOWALLA_DATASET:
        with open('softCosine_GOWALLA.pickle', 'rb') as handle:
            return pickle.load(handle)
    elif boolDataset == BRIGHTKITE_DATASET:
        with open('softCosine_BRIGHTKITE.pickle', 'rb') as handle:
            return pickle.load(handle)
    else:
        print 'Invalid dataset chosen'
        exit(1)

#dic = getPickleDic(BRIGHTKITE_DATASET)

def get_soft_cosine(userInterestList):
    global dic
    key = hash(tuple(userInterestList))
    if isnan(dic[key]):
        return 0.0
    else:
        return dic[key]

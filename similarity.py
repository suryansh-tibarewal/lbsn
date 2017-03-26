import numpy as np
from similarityMatrixGenerator import getInterestList
from math import sqrt

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
def get_soft_cosine(v1, v2):
    global matrix, interestList
    X = vectorize(v1, interestList)
    Y = vectorize(v2, interestList)
    return soft_cosine(X, Y, matrix)

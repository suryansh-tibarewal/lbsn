from similarity import get_soft_cosine2
from constants import eventType
import pickle
from maths import influence
from constants import BRIGHTKITE_DATASET, GOWALLA_DATASET, NEG_INF
import math
import user_object

def saveUserListtoFile(boolDataset):
    if boolDataset == GOWALLA_DATASET:
        user_list = user_object.main(GOWALLA_DATASET)
        #print user_list
        with open('user_list_GOWALLA_DATASET.pickle', 'wb') as handle:
            pickle.dump(user_list, handle, protocol = pickle.HIGHEST_PROTOCOL)

    elif boolDataset == BRIGHTKITE_DATASET:
        user_list = user_object.main(BRIGHTKITE_DATASET)
        #print user_list
        with open('user_list_BRIGHTKITE_DATASET.pickle', 'wb') as handle:
            pickle.dump(user_list, handle, protocol = pickle.HIGHEST_PROTOCOL)
    else:
        print 'Invalid dataset chosen'
        exit(1)


def getSoftCosineDic(boolDataset):
    dic = {}
    user_list = user_object.getUserListFromFile(boolDataset)
    #print user_list
    for user in user_list:
        #print 'starts'
        posInterestList = tuple(user_list[user]['interests_list'])
        #hashKey = hash(tuple(interestList))
        if posInterestList not in dic:
            dic[posInterestList] = get_soft_cosine2(eventType, posInterestList)
        negInterestList = tuple(user_list[user]['neg_interests_list'])
        #hashKey = hash(tuple(negInterestList))
        if negInterestList not in dic:
            dic[negInterestList] = get_soft_cosine2(eventType, negInterestList)
        totInterestList = tuple([tuple(posInterestList), tuple(negInterestList)])
        #hashKey = hash(tuple([tuple(interestList), tuple(negInterestList)]))
        if totInterestList not in dic:
            dic[totInterestList] = get_soft_cosine2(eventType, posInterestList, negInterestList)
        #print 'ends'

    return dic

def saveSoftCosinetoFile(boolDataset):
    dic = getSoftCosineDic(boolDataset)
    if boolDataset == GOWALLA_DATASET:
        with open('softCosine_GOWALLA.pickle', 'wb') as handle:
            pickle.dump(dic, handle, protocol = pickle.HIGHEST_PROTOCOL)
    elif boolDataset == BRIGHTKITE_DATASET:
        with open('softCosine_BRIGHTKITE.pickle', 'wb') as handle:
            pickle.dump(dic, handle, protocol = pickle.HIGHEST_PROTOCOL)
    else:
        print 'Invalid dataset chosen'
        exit(1)

saveSoftCosinetoFile(BRIGHTKITE_DATASET)
print 'done'
saveSoftCosinetoFile(GOWALLA_DATASET)
print 'done'
#saveUserListtoFile(GOWALLA_DATASET)
#saveUserListtoFile(BRIGHTKITE_DATASET)
#getSoftCosineDic(BRIGHTKITE_DATASET)
#print getSoftCosineDic(BRIGHTKITE_DATASET)

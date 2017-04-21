from similarity import get_soft_cosine2
from constants import eventType
import pickle
#from maths import influence
from constants import BRIGHTKITE_DATASET, GOWALLA_DATASET, NEG_INF
import math
import user_object

def saveUserListtoFile(boolDataset):
    if boolDataset == GOWALLA_DATASET:
        user_list = user_object.main(GOWALLA_DATASET)
        #print user_list
        if NEG_INF:
            with open('user_list_GOWALLA_DATASET_NEGINF.pickle', 'wb') as handle:
                pickle.dump(user_list, handle, protocol = pickle.HIGHEST_PROTOCOL)
        else:
            with open('user_list_GOWALLA_DATASET.pickle', 'wb') as handle:
                pickle.dump(user_list, handle, protocol = pickle.HIGHEST_PROTOCOL)

    elif boolDataset == BRIGHTKITE_DATASET:
        user_list = user_object.main(GOWALLA_DATASET)
        #print user_list
        if NEG_INF:
            with open('user_list_BRIGHTKITE_DATASET_NEGINF.pickle', 'wb') as handle:
                pickle.dump(user_list, handle, protocol = pickle.HIGHEST_PROTOCOL)
        else:
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
        interestList = user_list[user]['interests_list']
        hashKey = hash(tuple(interestList))
        dic[hashKey] = get_soft_cosine2(eventType, interestList)
        if NEG_INF:
            negInterestList = user_list[user]['neg_interests_list']
            hashKey = hash(tuple(interestList))
            dic[hashKey] = get_soft_cosine2(eventType, negInterestList)
            hashKey = hash(tuple([tuple(interestList), tuple(negInterestList)]))
            dic[hashKey] = get_soft_cosine2(eventType, interestList, negList = negInterestList)
        #print 'ends'

    return dic

def saveSoftCosinetoFile(boolDataset):
    dic = getSoftCosineDic(boolDataset)
    if boolDataset == GOWALLA_DATASET:
        if NEG_INF:
            with open('softCosine_GOWALLA_NEGINF.pickle', 'wb') as handle:
                pickle.dump(dic, handle, protocol = pickle.HIGHEST_PROTOCOL)
        else:
            with open('softCosine_GOWALLA.pickle', 'wb') as handle:
                pickle.dump(dic, handle, protocol = pickle.HIGHEST_PROTOCOL)

    elif boolDataset == BRIGHTKITE_DATASET:
        if NEG_INF:
            with open('softCosine_BRIGHTKITE_NEGINF.pickle', 'wb') as handle:
                pickle.dump(dic, handle, protocol = pickle.HIGHEST_PROTOCOL)
        else:
            with open('softCosine_BRIGHTKITE.pickle', 'wb') as handle:
                pickle.dump(dic, handle, protocol = pickle.HIGHEST_PROTOCOL)

    else:
        print 'Invalid dataset chosen'
        exit(1)

#saveSoftCosinetoFile(BRIGHTKITE_DATASET)
#print 'done'
#saveSoftCosinetoFile(GOWALLA_DATASET)
#print 'done'
#saveUserListtoFile(GOWALLA_DATASET)
#saveUserListtoFile(BRIGHTKITE_DATASET)
#getSoftCosineDic(BRIGHTKITE_DATASET)
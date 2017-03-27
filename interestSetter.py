from similarity import get_soft_cosine2
from constants import eventType
import pickle
from maths import influence
from constants import BRIGHTKITE_DATASET, GOWALLA_DATASET
import math
import user_object

def saveUserListtoFile(boolDataset):
    if boolDataset == GOWALLA_DATASET:
        user_list = user_object.main(GOWALLA_DATASET)
        with open('user_list_GOWALLA_DATASET.pickle', 'wb') as handle:
            pickle.dump(user_list, handle, protocol = pickle.HIGHEST_PROTOCOL)
    elif boolDataset == BRIGHTKITE_DATASET:
        user_list = user_object.main(GOWALLA_DATASET)
        with open('user_list_BRIGHTKITE_DATASET.pickle', 'wb') as handle:
            pickle.dump(user_list, handle, protocol = pickle.HIGHEST_PROTOCOL)
    else:
        print 'Invalid dataset chosen'
        exit(1)


def getSoftCosineDic(boolDataset):
    dic = {}
    user_list = user_object.getUserListFromFile(boolDataset)
    for user in user_list:
        interestList = user_list[user]['interests_list']
        hashKey = hash(tuple(interestList))
        dic[hashKey] = get_soft_cosine2(eventType, interestList)
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
saveSoftCosinetoFile(GOWALLA_DATASET)

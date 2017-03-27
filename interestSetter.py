from simulation import getUserList
from similarity import get_soft_cosine2
from constants import eventType
import pickle
from maths import influence
from constants import iMax1, p1
import math

user_list = getUserList()
#print user_list
dic = {}
print 'p1 = ', p1
for user in user_list:
    interestList = user_list[user]['interests_list']
    print interestList
    dic[hash(tuple(interestList))] = get_soft_cosine2(eventType, interestList)
    if math.isnan(dic[hash(tuple(interestList))]):
        print 'hello'
#with open('softCosine.pickle', 'wb') as handle:
#    pickle.dump(dic, handle, protocol = pickle.HIGHEST_PROTOCOL)

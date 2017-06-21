import mcl_clustering
import numpy as np
import networkx as nx
from collections import defaultdict
from constants import BRIGHTKITE_DATASET, GOWALLA_DATASET ,eventType , NEG_ONLY , mean,pos_interest_mul , neg_interest_mul
import pickle
from similarityMatrixGenerator import getInterestList
from similarity import getSimilarityMatrix
import numpy as np
import user_object

user_list = user_object.getUserListFromFile(BRIGHTKITE_DATASET)
interest_list = getInterestList('interests_list.txt')
print (interest_list)
popular_interests_list = [0]*len(interest_list)
neg_popular_interests_list = [0]*len(interest_list)
similarityMatrix = getSimilarityMatrix('similarityMatrix.txt')
event_interest_count = [0]*len(interest_list)
eventType = ['Classes']
for eventType in eventType:
    event_interest_count[interest_list.index(eventType)]+=1

# for user in user_list:
#     for interest in user_list[user]['interests_list']:
#         popular_interests_list[interest_list.index(interest)]+=1
# #print (popular_interests_list)
#
# for user in user_list:
#     for interest in user_list[user]['neg_interests_list']:
#         popular_interests_list[interest_list.index(interest)]-=1
#
# print (popular_interests_list)
#print (neg_popular_interests_list)


group_interest_count = [0]*len(interest_list)
num = 0
group = [7986, 44474, 21546]
for user in group:
    print ('%s + intrests : ',user,user_list[user]['interests_list'])
    print ('%s - intrests : ',user,user_list[user]['neg_interests_list'])


group_interest_count = [0]*len(interest_list)
num = 0
for user in group:
    pos = user_list[user]['interests_list']
    neg = user_list[user]['neg_interests_list']
    for p in pos:
        group_interest_count[interest_list.index(p)]+=pos_interest_mul
    for n in neg:
        group_interest_count[interest_list.index(n)]-=neg_interest_mul

print (group_interest_count)

for i in range (len(interest_list)):
    for j in range (len(interest_list)):
        num += similarityMatrix[i][j]*group_interest_count[i]*event_interest_count[j]
print (num)

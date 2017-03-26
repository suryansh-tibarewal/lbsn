#shitty import random
import random
from constants import BRIGHTKITE_DATASET, GOWALLA_DATASET
import return_pos_time
from return_pos_time import neg, usersInRegion
from simulation import F
import numpy as np

def generateRandomList(start, end, num):
    return np.random.uniform(start, end, num).tolist()


x_coordinates = generateRandomList(0.5, 0.6, 12)
y_coordinates = generateRandomList(0.45, 0.55, 12)

C = list()
i=0
while i<12:
    pos = (x_coordinates[i], y_coordinates[i])
    C.append(pos)
    i = i+1
Ns = 10
Ni = 10
delta = 0.1
alpha = 2

return_pos_time.initialize(BRIGHTKITE_DATASET)

#shitty function minJ
def minJ(P, rand):
    global Ns
    den = summation(0,Ns,P)
    for j in range(0,Ns):
        num = summation(0, j, P)
        if den==0:
            continue
        expr = float(num)/float(den)
        if expr >= rand:
            return j
    return -1
    exit(1)

#shitty function summation
def summation(i, j, P):
    s = 0
    for k in range(i, j):
        s += F(P[k])
        #print 's:',s
    return s

def getRandomTime(time1, time2):
    return random.uniform(time1, time2)

def Fdash(user_object, graph_object):
    global E_t0, E_r0, init_pro, add_pro
    randTime = getRandomTimeStamp(E_t0 + init_pro, E_t0 + init_pro + add_pro) ############

    sum = 0
    for user in usersInRegion(pos[0], pos[1], E_r0, randTime):
        term1 = len(graph_object.getFriends(user))
        innerSum = 0
        phyWorldFriends = neg(user, randTime)
        for v in phyWorldFriends:
            innerSum += len(graph_object.getFriends(v))
        term2 = float(innerSum)/len(phyWorldFriends)
        sum += term1 + term2

    return sum

#############################################################################################################################


def dis(loc1, loc2):
    from maths import eucledianDist
    return eucledianDist(loc1[0], loc1[1], loc2[0], loc2[1])

P = list()
Nc = []
for i in range(Ns):
    Nc.append(0)
    while True:
        r = random.choice(C)
        if r not in P:
            break
    P.append(r)

#print 'P: ', P
#print 'Nc: ', Nc


maxF = -1
resPos = []
# rand = random.uniform(0, 1)
# print 'rand' , rand
# new = minJ(P,rand)
# print 'new:',new

for i in range(Ni):
    rand = random.uniform(0, 1)
    j = minJ(P, rand)
    delta = float(delta)/pow(alpha, Nc[j])
    delta = float(delta)/pow(alpha, Nc[j])
    newC = []
    for pos in C:
        if(dis(pos, P[j]) <= delta):
            newC.add(pos)
    posNew = random.choice(newC)
    currF = F(posNew)
    if currF > F(P[j]):
        P[j] = posNew
    Nc[j] += 1

max1 = Nc[0]

print 'Nc:' , Nc

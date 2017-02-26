#shitty import random
import random

C = (1, 2, 3, 4, 5, 6, 7, 8, 9 , 10)
Ns = 10 
Ni = 10
delta = 0.1
alpha = 2

#shitty function minJ
def minJ(P, rand):
	global Ns
	for j in range(Ns):
		num = summation(1, j, P)
		den = num + summation(j+1, Ns, P)
		expr = float(num)/den
		if expr > rand:
			return j
	else:
		print 'minJ should return value less than Ns = ', Ns
		exit(1)

#shitty function summation
def summation(i, j, P):
	s = 0
	for k in range(i, j+1):
		sum += F(P[k])
	
	return s


############################################################################################################################
def neg(uid, t):
	#returns list of users who are friends in physical world of uid at time t


def F(pos):
	#returns number of influenced users
	#pos is a list of two values with pos[0] as x-coordinate and pos[1] as y-coordinate
	#this function is simulation

def getRandomTime(time1, time2):
	#returns a random timeStamp(actual timeStamp from data) between two timeStamps both exclusive
	#time recieved in normalized form
	
def usersInRegion(x, y, r, t):
	#returns a list of all users who are in the circular region made by x, y and r at time t


#############################################################################################################################

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

P = set()
Nc = []
for i in range(Ns):
	Nc.append(0)
	while True:
		r = random.choice(candidateSet)
		if r not in selectedSet:
			break
	P.add(r)

print 'P: ', P
print 'Nc: ', Nc


maxF = -1
resPos = []
for i in range(Ni):
	rand = random.random()
	j = minJ(P, rand)
	delta = float(delta)/pow(alpha, Nc[j])
	newC = set()
	for pos in C:
		if(dis(pos, P[j]) <= delta):
			newC.add(pos)
	posNew = random.choice(newC)
	currF = F(posNew)
	if currF > F(P[j]):
		P[j] = posNew
	if currF > maxF:
		maxF = currF
		resPos[0] = posNew[0]
		resPos[1] = posNew[1]
	Nc[j] += 1


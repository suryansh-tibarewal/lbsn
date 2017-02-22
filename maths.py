from math import sqrt
from random import random

iMax1 = 3
iMax2 = 1.5
iMax3 = 6
c = 5

init_pro = 0.02
maxDescriptionCount = 10

p1 = 
p2 = 
p3 = 
p4 = 
p5 = 

propRad = 


def eucledianDist(ux, uy, vx, vy):
	dist = sqrt(pow(vx - ux, 2) + pow(vy - uy, 2))
	return dist

def influence(x, iMax):
	inf = (iMax - 1)*sqrt(1 - pow(1 - x, 2)) + 1
	return inf

def jaccardCoeff(a, b):
	coeff = len(a & b)/len(a | b)
	return coeff

def interestMatchInf(eventType, userIntereset):
	global iMax1
	jaccCoeff = jaccardCoeff(eventType, userInterest)
	i1 = influence(jaccCoeff, iMax1)
	return i1

def regionStayInf(stayTime):
	global  iMax2, init_pro
	normalizedStayTime = stayTime/init_pro
	i2 = influence(normalizedStayTime, iMax2)
	return i2

def recievedCopiesInf(descriptionCount)
	global iMax3, maxDescriptionCount
	exp = (descriptionCount - 1)/maxDescriptionCount
	i3 = influence(min(exp, 1), iMax3)
	return i3

def friendInf(isFriend):
	global c
	if isFriend:
		return c
	else:
		return 1

def init_inf_prob(eventType, userInterest, stayTime):
	global p1, iMax1, iMax2
	i1 = interestMatchInf(eventType, userInterest)
	i2 = regionStayInf(stayTime)
	p = min(p1*i1*i2, 1)
	return p

def osn_share_prob(eventType, userInterest):
	global p2, iMax1
	i1 = interestMatchInf(eventType, userInterest)
	p = min(p2*i1, 1)
	return p

def osn_inf_prob(eventType, userInterest, descriptionCount):
	global p3, iMax1, iMax3
	i1 = interestMatchInf(eventType, userInterest)
	i3 = recievedCopiesInf(descriptionCount)
	p = min(p3*i1*i3, 1)
	return p


def pw_share_prob(eventType, userInterest):
	global p4, iMax1
	i1 = interestMatchInf(eventType, userInterest)
	p = min(p4*i1, 1)
	return p

def phy_inf_prob(eventType, userInterest, isFriend):
	global p5, iMax1
	i1 = interestMatchInf(eventType, userInterest)
	i4 = friendInf(isFriend)
	p = min(p5*i1*i4, 1)
	return p


######################################################################

def arePhysicalWorldNeighbors(ux, uy, vx, vy):
	global propRad
	ans = False
	if euclideanDist(ux, uy, vx, vy) <= propRad
		ans = True
	return ans

def insideRegion(xCen, yCen, r, x, y):
	ans = False
	if pow(x - xCen, 2) + pow(y - yCen, 2) <= pow(r, 2)
		ans = True
	return ans

def nodesInsideRegion(xCen, yCen, r):
	res = []
	for v in G:
		if insideRegion(xCen, yCen, r, vx, vy):
			res.append(v)
	return res

def stayTimeinRegion(xCen, yCen, r):
	global init_pro
	r = range(0, 1, jump)
	for t in r:
		
	
	
#####################################################################

#initial influence propagation
ini = nodesInsideRegion()
influenced = []
for v in ini:
	T = stayTimeinRegion(E.x0, E.y0, E.r0)
	p = init_inf_prob(E.type, v.interest, T)
	rand = random()
	if rand <= p:
		influenced.append(v)
	
#influence propagation in OSN
sharing = []
for v in influenced:
	p = osn_share_prob(E.type, v.interest)
	rand = random()
	if rand <= p:
		sharing.append(v)

for v in sharing:
	
			
	
	

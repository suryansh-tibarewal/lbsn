from math import sqrt
from random import random

from constants import *


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
	global i_max1
	jaccCoeff = jaccardCoeff(eventType, userInterest)
	i1 = influence(jaccCoeff, i_max1)
	return i1

def regionStayInf(stayTime):
	global  i_max2, init_pro
	normalizedStayTime = stayTime/init_pro
	i2 = influence(normalizedStayTime, i_max2)
	return i2

def recievedCopiesInf(descriptionCount)
	global iMax3, n_max
	exp = (descriptionCount - 1)/n_max
	i3 = influence(min(exp, 1), i_max3)
	return i3

def friendInf(isFriend):
	global c
	if isFriend:
		return c
	else:
		return 1

def init_inf_prob(eventType, userInterest, stayTime):
	global p1, i_max1, i_max2
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
	global p3, i_max1, i_max3
	i1 = interestMatchInf(eventType, userInterest)
	i3 = recievedCopiesInf(descriptionCount)
	p = min(p3*i1*i3, 1)
	return p


def pw_share_prob(eventType, userInterest):
	global p4, i_max1
	i1 = interestMatchInf(eventType, userInterest)
	p = min(p4*i1, 1)
	return p

def phy_inf_prob(eventType, userInterest, isFriend):
	global p5, i_max1
	i1 = interestMatchInf(eventType, userInterest)
	i4 = friendInf(isFriend)
	p = min(p5*i1*i4, 1)
	return p


######################################################################

def arePhysicalWorldNeighbors(ux, uy, vx, vy):
	global propRad
	ans = False
	if euclideanDist(ux, uy, vx, vy) <= propRad:
		ans = True
	return ans

def insideRegion(xCen, yCen, r, x, y):
	ans = False
	if pow(x - xCen, 2) + pow(y - yCen, 2) <= pow(r, 2):
		ans = True
	return ans

def nodesInsideRegion(xCen, yCen, r):
	res = []
	for v in G:
		if insideRegion(xCen, yCen, r, vx, vy):
			res.append(v)
	return res
	
	
####################################################################
	
	

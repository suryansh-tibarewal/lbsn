from math import sqrt
from random import random
from similarity import get_soft_cosine
from constants import *

global P1, P2, P3, P4, P5

def eucledianDist(ux, uy, vx, vy):
    dist = sqrt(pow(vx - ux, 2) + pow(vy - uy, 2))
    return dist

def influence(x, iMax):
    #print x, iMax
    inf = (iMax - 1)*sqrt(1 - pow(1 - x, 2)) + 1
    #print "inf", inf
    return inf

def jaccardCoeff(a, b):
    coeff = len(set(a) & set(b))/len(set(a) | set(b))
    return coeff

def interestMatchInf(eventType, userInterest):
    global iMax1
    jaccCoeff = jaccardCoeff(eventType, userInterest)
    #softCoeff = get_soft_cosine(eventType, userInterest)
    #print softCoeff
    i1 = influence(jaccCoeff, iMax1)
    return i1

def regionStayInf(stayTime):
    global  iMax2, init_pro
    normalizedStayTime = stayTime/init_pro
    i2 = influence(normalizedStayTime, iMax2)
    return i2

def recievedCopiesInf(descriptionCount):
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
    global P1, iMax1, iMax2
    P1 = getP1()
    i1 = interestMatchInf(eventType, userInterest)
    i2 = regionStayInf(stayTime)
    P = min(P1*i1*i2, 1)
    return P

def osn_share_prob(eventType, userInterest):
    global P2, iMax1
    P2 = getP2()
    i1 = interestMatchInf(eventType, userInterest)
    P = min(P2*i1, 1)
    return P

def osn_inf_prob(eventType, userInterest, descriptionCount):
    global P3, iMax1, iMax3
    P3 = getP3()
    i1 = interestMatchInf(eventType, userInterest)
    i3 = recievedCopiesInf(descriptionCount)
    P = min(P3*i1*i3, 1)
    return P


def pw_share_prob(eventType, userInterest):
    global P4, iMax1
    P4 = getP4()
    i1 = interestMatchInf(eventType, userInterest)
    P = min(P4*i1, 1)
    return P

def phy_inf_prob(eventType, userInterest, isFriend):
    global P5, iMax1
    P5 = getP5()
    i1 = interestMatchInf(eventType, userInterest)
    i4 = friendInf(isFriend)
    P = min(P5*i1*i4, 1)
    return P


######################################################################

def arePhysicalWorldNeighbors(ux, uy, vx, vy):
    global propRad
    ans = False
    if euclideanDist(ux, uy, vx, vy) <= propRad:
        ans = True
    return ans

def insideRegion(xCen, yCen, r, x, y):
    ans = False
    #print xCen, yCen, r, x, y
    if (pow(x - xCen, 2) + pow(y - yCen, 2)) <= pow(r, 2):
        print "yoda"
        ans = True
    return ans

def nodesInsideRegion(xCen, yCen, r):
    res = []
    for v in G:
        if insideRegion(xCen, yCen, r, vx, vy):
            res.append(v)
    return res

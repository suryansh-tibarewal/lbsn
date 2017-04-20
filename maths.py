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

def newP(baseP, i1, i2):
    t1 = max(abs(i1), abs(i2))
    t21 = min(abs(i1), abs(i2))
    t22 = (float(i1*i2)) / (abs(i1*i2))
    t2 = pow(t21, t22)
    t3 = float(i1 + i2) / abs(i1 + i2)
    P = baseP*t1*t2*t3
    return P

def jaccardCoeff(a, b):
    coeff = len(set(a) & set(b))/len(set(a) | set(b))
    return coeff

def interestMatchInf(eventType, userInterest, negUserInterest):
    #print 'interestMatchInf'
    global iMax1
    #jaccCoeff = jaccardCoeff(eventType, userInterest)

    softCoeff = get_soft_cosine(userInterest, negUserInterest)
    #print softCoeff
    i1 = influence(abs(softCoeff), iMax1)
    return i1*w1

def regionStayInf(stayTime):
    global  iMax2, init_pro
    normalizedStayTime = stayTime/init_pro
    i2 = influence(normalizedStayTime, iMax2)
    return i2*w2

def recievedCopiesInf(descriptionCount):
    global iMax3, maxDescriptionCount
    if descriptionCount == 0:
        return 0.0
    exp = float(descriptionCount)/maxDescriptionCount
    i3 = influence(min(exp, 1), iMax3)
    return i3*w3

def friendInf(friendPolarity):
    global c
    if friendPolarity == 0:
        return float(1)*w4
    else:
        return float(c*friendPolarity)*w4

def init_inf_prob(eventType, userInterest, stayTime, negUserInterest = None):
    #print 'init_inf_prob'
    global P1, iMax1, iMax2
    P1 = getP1()
    i1 = interestMatchInf(eventType, userInterest, negUserInterest)
    i2 = regionStayInf(stayTime)
    if negUserInterest is None:
        P = min(P1*i1*i2, 1)
        #print 'oldP used'
    else:
        P = min(newP(P1, i1, i2), 1)
        #print 'newP used'
    return P

def osn_share_prob(eventType, userInterest):
    global P2, iMax1
    P2 = getP2()
    i1 = interestMatchInf(eventType, userInterest, None)
    P = min(P2*i1, 1)
    return P

def osn_inf_prob(eventType, userInterest, descriptionCount, negUserInterest = None):
    global P3, iMax1, iMax3
    P3 = getP3()
    i1 = interestMatchInf(eventType, userInterest)
    i3 = recievedCopiesInf(descriptionCount)
    if negUserInterest is None:
        P = min(P3*i1*i3, 1)
    else:
        P = min(newP(P3, i1, i3), 1)
    return P


def pw_share_prob(eventType, userInterest):
    global P4, iMax1
    P4 = getP4()
    i1 = interestMatchInf(eventType, userInterest, None)
    P = min(P4*i1, 1)
    return P

def phy_inf_prob(eventType, userInterest, friendPolarity, negUserInterest = None):
    global P5, iMax1
    P5 = getP5()
    i1 = interestMatchInf(eventType, userInterest)
    i4 = friendInf(friendPolarity)
    if negUserInterest is None:
        P = min(P5*i1*i4, 1)
    else:
        P = min(newP(P5, i1, i4), 1)
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
    if (pow(x - xCen, 2) + pow(y - yCen, 2)) <= pow(r, 2):
        ans = True
    return ans

def nodesInsideRegion(xCen, yCen, r):
    res = []
    for v in G:
        if insideRegion(xCen, yCen, r, vx, vy):
            res.append(v)
    return res

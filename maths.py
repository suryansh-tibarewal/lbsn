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
    if i1 == 0 or i2 == 0:
        return 0.

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
    polarity = 1
    if softCoeff != 0:
        polarity = softCoeff/abs(softCoeff)
    i1 = influence(abs(softCoeff), iMax1)
    i1 = i1 * polarity
    return i1*w1

def numberOfLoginsInf(numberOfLogins, maximumValue):
    global iMax2dash, init_pro
    normalizedValue =  numberOfLogins/maximumValue
    i2dash = influence(normalizedValue, iMax2dash)
    return i2dash*w2dash

def regionStayInf(stayTime):
    global  iMax2, init_pro
    normalizedStayTime = stayTime/init_pro
    i2 = influence(normalizedStayTime, iMax2)
    return i2*w2

def recievedCopiesInf(descriptionCount, negDescriptionCount):
    global iMax3, maxDescriptionCount
    if negDescriptionCount is None:
        if descriptionCount == 0:
            return 0.0
        exp = float(descriptionCount - 1)/maxDescriptionCount
    else:
        if descriptionCount == 0 and negDescriptionCount == 0:
            return 0.0
        exp = float(descriptionCount - negDescriptionCount)/maxDescriptionCount
    polarity = 1
    if exp != 0:
        polarity = exp/abs(exp)
    exp = abs(exp)
    i3 = influence(min(exp, 1), iMax3)
    return i3*w3*polarity

def friendInf(isFriend, friendPolarity):
    global c
    if friendPolarity is None:
       friendPolarity = 1
    if isFriend:
        return friendPolarity*c*w4
    else:
        return friendPolarity*1*w4

def init_inf_prob(eventType, userInterest, stayTime, negUserInterest = None):
    #print 'init_inf_prob'
    global P1, iMax1, iMax2
    P1 = getP1()
    i1 = interestMatchInf(eventType, userInterest, negUserInterest)
    i2 = regionStayInf(stayTime)
    prob = newP(P1, i1, i2)
    if prob > 1:
        P = min(prob, 1.)
    elif prob < -1:
        P = max(prob, -1.)
    else:
        P = prob
    return P

def online_init_inf_prob(eventType, userInterest, numberOfLogins, maximumValue, negUserInterest = None):
    #print 'init_inf_prob'
    global P1, iMax1, iMax2dash
    P1 = getP1()
    i1 = interestMatchInf(eventType, userInterest, negUserInterest)
    i2dash = numberOfLoginsInf(numberOfLogins, maximumValue)
    prob = newP(P1, i1, i2dash)
    if prob > 1:
        P = min(prob, 1.)
    elif prob < -1:
        P = max(prob, -1.)
    else:
        P = prob
    return P

def osn_share_prob(eventType, userInterest):
    global P2, iMax1
    P2 = getP2()
    i1 = interestMatchInf(eventType, userInterest, None)
    P = min(P2*i1, 1)
    return P

def osn_inf_prob(eventType, userInterest, descriptionCount, negUserInterest = None, negDescriptionCount = None):
    global P3, iMax1, iMax3
    P3 = getP3()
    i1 = interestMatchInf(eventType, userInterest, negUserInterest)
    i3 = recievedCopiesInf(descriptionCount, negDescriptionCount)
    prob = newP(P1, i1, i3)
    if prob > 1:
        P = min(prob, 1.)
    elif prob < -1:
        P = max(prob, -1.)
    else:
        P = prob
    return P


def pw_share_prob(eventType, userInterest):
    global P4, iMax1
    P4 = getP4()
    i1 = interestMatchInf(eventType, userInterest, None)
    P = min(P4*i1, 1)
    return P

def phy_inf_prob(eventType, userInterest, isFriend, negUserInterest = None, friendPolarity = None):
    global P5, iMax1
    P5 = getP5()
    i1 = interestMatchInf(eventType, userInterest, negUserInterest)
    i4 = friendInf(isFriend, friendPolarity)
    prob = newP(P1, i1, i4)
    if prob > 1:
        P = min(prob, 1.)
    elif prob < -1:
        P = max(prob, -1.)
    else:
        P = prob
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

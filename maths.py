from math import sqrt
from random import random

iMax1 = 3
iMax2 = 1.5
iMax3 = 6
c = 5

init_pro = 0.02
maxDescriptionCount = 10

p1 = 0.5
p2 = 0.5
p3 = 0.5 
p4 = 0.5
p5 = 0.5

propRad = 0.01


def eucledianDist(ux, uy, vx, vy):
    dist = sqrt(pow(vx - ux, 2) + pow(vy - uy, 2))
    return dist

def influence(x, iMax):
    inf = (iMax - 1)*sqrt(1 - pow(1 - x, 2)) + 1
    #print "inf", inf
    return inf

def jaccardCoeff(a, b):
    coeff = len(set(a) & set(b))/len(set(a) | set(b))
    return coeff

def interestMatchInf(eventType, userInterest):
    global iMax1
    jaccCoeff = jaccardCoeff(eventType, userInterest)
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
    
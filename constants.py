BRIGHTKITE_DATASET = 0
GOWALLA_DATASET = 1

init_on = True
osn_on = True
pw_on = True


iMax1 = 3
iMax2 = 1.5
iMax3 = 6
c = 5
init_pro = 0.02
add_pro = 0.2
maxDescriptionCount = 10
e_t0 = 0.5
e_r0 = 0.01

e_lat = 0.3422742228921536
e_lon = 0.09916773323165684

# p should lie between 0 and 2/3
p = 0.42
p1 = p
p2 = 1.5*p
p3 = 1.5*p
p4 = 1.5*p
p5 = 1.5*p

rp = 0.01

buffer_time = 0.000000001

def recalculateProbs():
    global p1, p2, p3, p4, p5
    p1 = p
    p2 = 1.5*p
    p3 = 1.5*p
    p4 = 1.5*p
    p5 = 1.5*p
    #print p1, p2, p3, p4, p5

def setP(value):
    global p
    if value < 0 or value > 2.0/3:
        print 'Influencing prob shoulb be between 0 and 2/3'
        exit(1)
    p = value
    recalculateProbs()

def setInitPro(value):
    global init_pro
    init_pro = value

def getSwitchStatus():
    global init_on, osn_on, pw_on
    res = []
    res.extend([init_on, osn_on, pw_on])
    return res

def setAddPro(value):
    global add_pro
    add_pro = value

def setInitInfReg(value):
    global e_r0
    e_r0 = value

def switchInitOn(boolVal):
    global init_on
    init_on = boolVal

def switchOsnOn(boolVal):
    #print boolVal
    global osn_on
    print "bool", boolVal
    osn_on = boolVal
    print "tud", osn_on

def switchPwOn(boolVal):
    #print boolVal
    global pw_on
    pw_on = boolVal
    #print "hhn", pw_on

def getSwitchStatus():
    global init_on, osn_on, pw_on
    res = []
    res.extend([init_on, osn_on, pw_on])
    return res

def setEventPos(eventLon, eventLat):
    global e_lon, e_lat
    e_lon = eventLon
    e_lat = eventLat

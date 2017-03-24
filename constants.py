BRIGHTKITE_DATASET = 0
GOWALLA_DATASET = 1

init_on = True
osn_on = True
pw_on = True

i_max1 = 3
i_max2 = 1.5
i_max3 = 6
c = 5
init_pro = 0.02
add_pro = 0.2
n_max = 10
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

buffer_time = 0.0001

def recalculateProbs():
    global p1, p2, p3, p4, p5
    p1 = p
    p2 = 1.5*p
    p3 = 1.5*p
    p4 = 1.5*p
    p5 = 1.5*p

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
    global osn_on
    osn_on = boolVal

def switchPwOn(boolVal):
    global pw_on
    pw_on = boolVal

def setEventPos(eventLon, eventLat):
    global e_lon, e_lat
    e_lon = eventLon
    e_lat = eventLat

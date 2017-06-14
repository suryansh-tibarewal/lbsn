import checkIn_object
import user_object
from user_object import setGradientTimeList
from constants import *
import graph_object
from maths import osn_share_prob, osn_inf_prob, pw_share_prob, phy_inf_prob, insideRegion, online_init_inf_prob, init_inf_prob, eucledianDist
import random
import time
from operator import itemgetter
from return_pos_time import get_pos
import return_pos_time
from clustering import get_clusters, get_optimal_cluster


random.seed(10)

global influenced_list, checkIn_list, n_users

global initOn, osnOn, pwOn
global initPro, addPro, eR0

#influenced_bit = 0
user_list = user_object.getUserListFromFile(BRIGHTKITE_DATASET, NEG_ONLY) ####new value
#print 8472 in user_list.keys()
#if 8472 in user_list.keys():
    #print "yo3"

def social_check(checkIn_entry , influenced):
    global eventType
    user_id_receiver = checkIn_entry[0]
    checkIn_time = checkIn_entry[1]
    description_count = 0
    neg_description_count = 0
    for user_id_sender in influenced:
        if not user_list[user_id_sender]['online_shared']:
            continue
        if(graph_object.checkUnDirectedEdge(user_id_sender, user_id_receiver)):
            time_of_influence_sender = user_list[user_id_sender]['time_of_influence']
            if (time_of_influence_sender <= checkIn_time): # less than or less than equal to?
                    polarity = user_list[user_id_sender]['influenced_bit']
                    if polarity == 1:
                        description_count = description_count + 1
                    elif polarity == -1:
                        neg_description_count = neg_description_count + 1
    #print description_count, neg_description_count
    #if description_count > 0:   ####What is this ??????
    if NEG_INF:
        #print 'in NEG_INF1 :: ', user_list[user_id_receiver]['neg_interests_list']
        rec_prob = osn_inf_prob(eventType, user_list[user_id_receiver]['interests_list'], description_count, user_list[user_id_receiver]['neg_interests_list'], neg_description_count)
    else:
        rec_prob = osn_inf_prob(eventType, user_list[user_id_receiver]['interests_list'], description_count)
    if rec_prob != 0:
        #print "osn_inf_prob", rec_prob
        polarity = rec_prob/abs(rec_prob)
        rec_prob = abs(rec_prob)
        random_num = random.random()
        if random_num <= rec_prob:
            return polarity
    return 0

def offline_edge(user_id_sender, checkIn_entry, ind):
    global checkIn_list
    user_id_receiver = checkIn_entry[0]
    receiver_time = checkIn_entry[1]
    receiver_lat = checkIn_entry[2]
    receiver_lon = checkIn_entry[3]
    low_time = receiver_time - 0.00001
    high_time = receiver_time + 0.00001
    ind_val = ind
    while True:
        ind = ind - 1
        if ind<0 or low_time>checkIn_list[ind][1]:
            break
        if checkIn_list[ind][0] == user_id_sender:
            sender_lat = checkIn_list[ind][2]
            sender_lon = checkIn_list[ind][3]
            if insideRegion(sender_lon, sender_lat, rp, receiver_lon, receiver_lat):
                return ind
    ind = ind_val
    ind_high = len(checkIn_list)
    while True:
        ind = ind + 1
        if ind>=ind_high or high_time<checkIn_list[ind][1]:
            break
        if checkIn_list[ind][0] == user_id_sender:
            sender_lat = checkIn_list[ind][2]
            sender_lon = checkIn_list[ind][3]
            if insideRegion(sender_lon, sender_lat, rp, receiver_lon, receiver_lat):
                return ind
    return -1

def sharedTimeCheck(user_id, timestamp):
    global user_list
    time_list = user_list[user_id]['physical_share_time_list']
    for time in time_list:
        if (time<=(timestamp+ 0.0001) and time>=timestamp): #check the dependency with this buffer time
           return True
    return False

def physical_check(checkIn_entry , influenced, ind):
    global eventType
    global user_list
    user_id_receiver = checkIn_entry[0]
    checkIn_time = checkIn_entry[1]
    receiver_lat = checkIn_entry[2]
    receiver_lon = checkIn_entry[3]
    user_id_rejected_set = set()
    # do it user wise or checkIn wise
    for user_id_sender in influenced:
        if not user_list[user_id_sender]['offline_shared']:
            continue
        if (user_list[user_id_sender]['active'] == 0):
            continue
        #ind_s = offline_edge(user_id_sender, checkIn_entry, ind)
        sender_position = get_pos(user_id_sender, checkIn_time)
        try :
            val = sender_position[0]
        except:
            user_list[user_id_sender]['active'] == 0
            #print "not available", user_id_sender
            continue
        #print "Step4"
        if insideRegion(sender_position[0], sender_position[1], rp, receiver_lon, receiver_lat):
            #print "Step5"
            if not sharedTimeCheck(user_id_sender, checkIn_entry[1]):
                continue
            #print "step6"
            isFriend = graph_object.checkUnDirectedEdge(user_id_sender, user_id_receiver) ##change this??
            polarity = user_list[user_id_sender]['influenced_bit']
            if NEG_INF:
                rec_prob = phy_inf_prob(eventType, user_list[user_id_receiver]['interests_list'], isFriend, user_list[user_id_receiver]['neg_interests_list'], polarity)
            else:
                rec_prob = phy_inf_prob(eventType, user_list[user_id_receiver]['interests_list'], isFriend)
            if rec_prob!=0:
                #print "phy_inf_prob", rec_prob
                polarity = rec_prob/abs(rec_prob)
                rec_prob = abs(rec_prob)
                random_num = random.random()
                if random_num <= rec_prob:
                    #print "physical influence"
                    #exit(1)
                    return polarity
    return 0

def get_initial_users(event_lon, event_lat, rp, start_time, end_time):
    global checkIn_list
    users_set = set()
    count = 0
    for checkIn_entry in checkIn_list:
        user_id = checkIn_entry[0]
        if user_id in users_set:
            continue
        if checkIn_entry[1]>=start_time and checkIn_entry[1]<=end_time:
            count = count + 1
            #print "tuduk", event_lon, event_lat, rp, checkIn_entry[3], checkIn_entry[2]
            if insideRegion(event_lon, event_lat, rp, checkIn_entry[3], checkIn_entry[2]):
                users_set.add(checkIn_entry[0])
    print "check entries", count
    users_set = list(users_set)
    users_set.sort()
    return users_set

def get_online_initial_users(start_time, end_time):
    global checkIn_list
    users_set = set()
    clusters = get_clusters(BRIGHTKITE_DATASET)
    cluster = get_optimal_cluster(clusters)
    print cluster
    count = 0
    for checkIn_entry in checkIn_list:
        user_id = checkIn_entry[0]
        if user_id in users_set:
            continue
        if checkIn_entry[1]>=start_time and checkIn_entry[1]<=end_time:
            count = count + 1
            #print user_id
            #print "tuduk", event_lon, event_lat, rp, checkIn_entry[3], checkIn_entry[2]
            if user_id in cluster:
                users_set.add(user_id)
    print "check entries", count
    users_set = list(users_set)
    users_set.sort()
    return users_set

def initial_propogation(event_lon, event_lat, start_time, end_time):
    global eventType, influenced_list, user_list
    global initPro, eR0
    eR0 = getInitInfReg()
    initPro = getInitPro()
    users_region_list = list()
    users_online_region_list = list()
    if OFFLINE_EVENT:
        users_region_list = get_initial_users(event_lon, event_lat, eR0, start_time, end_time)  #TODO improvement get stayTimeInRegion here only
        print 'offline initial users :: ', users_region_list
    if ONLINE_EVENT:
        users_online_region_list = get_online_initial_users(start_time, end_time) #add parameter for cluster number later
        print 'online initial users ::', users_online_region_list
        maxLogins = getMaxLogins(start_time, end_time)
        print 'maxLogins in range :: ', maxLogins

    for user_id in users_online_region_list:
        numberOfLogins = getNumberOfLogins(start_time, end_time, user_id)
        print 'number of Logins for ' + str(user_id) + ' is ' + str(numberOfLogins)
        if NEG_INF:
            inf_prob = online_init_inf_prob(eventType, user_list[user_id]['interests_list'], numberOfLogins, maxLogins, user_list[user_id]['neg_interests_list'])
        else:
            inf_prob = online_init_inf_prob(eventType, user_list[user_id]['interests_list'], numberOfLogins, maxLogins)
        if inf_prob!=0:
            #print "init_inf", inf_prob
            polarity = inf_prob/abs(inf_prob)
            inf_prob = abs(inf_prob)
        print 'polarity for ' + str(user_id) + 'is :: ' + str(polarity)
        print 'inf_prob for ' + str(user_id) + 'is :: ' + str(inf_prob)
        random_num = random.random() # between 0 to 1
        print 'random number for ' + str(user_id) + 'is :: ' + str(random_num)
        if random_num <= inf_prob:
            user_list[user_id]['influenced_bit'] = polarity
            user_list[user_id]['time_of_influence'] = end_time
            influenced_list.append(user_id)
            #if user_list[user_id]['influenced_bit'] > 0:
            if polarity==1:
                online_share_prob = osn_share_prob(eventType, user_list[user_id]['interests_list'])
            elif polarity==-1 :
                online_share_prob = osn_share_prob(eventType, user_list[user_id]['neg_interests_list'])
            else:
                print "polarity is screwed in simulation.py in osn_share"
                exit(1)

            random_num = random.random() # between 0 to 1
            user_list[user_id]['physical_share_time_list'] = setGradientTimeList(end_time)
            if random_num <= online_share_prob:
                user_list[user_id]['online_shared'] = 1
            if polarity==1:
                offline_share_prob = pw_share_prob(eventType, user_list[user_id]['interests_list']) #improvement: should have position too
            elif polarity==-1:
                offline_share_prob = pw_share_prob(eventType, user_list[user_id]['neg_interests_list'])
            else:
                print "polarity is screwed in simulation.py in offline_share"
                exit(1)
            random_num = random.random()
            if random_num <= offline_share_prob:
                user_list[user_id]['offline_shared'] = 1

    for user_id in users_region_list:
        timeInRegion = stayTimeInRegion(event_lon, event_lat, eR0, e_t0, initPro, user_id)
        #print "user", user_id
        #print "check", user_list[user_id]
        if NEG_INF:
            #print 'hin NEG_INF :: ', user_list[user_id]['neg_interests_list']
            inf_prob = init_inf_prob(eventType, user_list[user_id]['interests_list'], timeInRegion, user_list[user_id]['neg_interests_list'])
            #print 'hello2'
        else:
            #print 'not in NEG_INF :: ', user_list[user_id]['neg_interests_list']
            inf_prob = init_inf_prob(eventType, user_list[user_id]['interests_list'], timeInRegion)
        if inf_prob!=0:
            #print "init_inf", inf_prob
            polarity = inf_prob/abs(inf_prob)
            inf_prob = abs(inf_prob)
        random_num = random.random() # between 0 to 1
        if random_num <= inf_prob:
            user_list[user_id]['influenced_bit'] = polarity
            user_list[user_id]['time_of_influence'] = end_time
            influenced_list.append(user_id)
            #if user_list[user_id]['influenced_bit'] > 0:
            if polarity==1:
                online_share_prob = osn_share_prob(eventType, user_list[user_id]['interests_list'])
            elif polarity==-1 :
                online_share_prob = osn_share_prob(eventType, user_list[user_id]['neg_interests_list'])
            else:
                print "polarity is screwed in simulation.py in osn_share"
                exit(1)
            #elif user_list[user_id]['influenced_bit'] < 0:
            #    online_share_prob = osn_share_prob(eventType, user_list[user_id]['neg_interests_list'])
            #else:
            #    print 'Error on calling online_share_prob in simulation.py'
            #    exit(1)
            random_num = random.random() # between 0 to 1
            user_list[user_id]['physical_share_time_list'] = setGradientTimeList(end_time)
            if random_num <= online_share_prob:
                user_list[user_id]['online_shared'] = 1
            if polarity==1:
                offline_share_prob = pw_share_prob(eventType, user_list[user_id]['interests_list']) #improvement: should have position too
            elif polarity==-1:
                offline_share_prob = pw_share_prob(eventType, user_list[user_id]['neg_interests_list'])
            else:
                print "polarity is screwed in simulation.py in offline_share"
                exit(1)
            random_num = random.random()
            if random_num <= offline_share_prob:
                user_list[user_id]['offline_shared'] = 1
    if not influenced_list:
        return None
    else:
        return True

def getTimeStampRegion(xCen, yCen, r, inside_point_x, inside_point_y, timestamp_1, outside_point_x, outside_point_y, timestamp_2):
    from shapely.geometry import LineString
    from shapely.geometry import Point
    center = Point(xCen,yCen)
    circle = center.buffer(r).boundary
    line = LineString([(inside_point_x, inside_point_y), (outside_point_x, outside_point_y)])
    boundary_points = circle.intersection(line)
    boundary_point_x = boundary_points.coords[0][0]
    boundary_point_y = boundary_points.coords[0][1]
    time_gap = timestamp_2 - (timestamp_1 + buffer_time)
    if(time_gap<0):
        time_gap = timestamp_2 - timestamp_1
    speed = (eucledianDist(outside_point_x , outside_point_y , inside_point_x , inside_point_y))/time_gap
    distance = eucledianDist(inside_point_x, inside_point_y, boundary_point_x, boundary_point_y)
    time = distance/speed
    return (timestamp_1 + time)

def getNumberOfLogins(start_time, end_time, user_id):
    global checkIn_list
    count = 0
    for checkIn_entry in checkIn_list:
        if (checkIn_entry[0] == int(user_id)) and (checkIn_entry[1]>=start_time and checkIn_entry[1]<=end_time):
            count += 1
    return count

def getMaxLogins(start_time, end_time):
    global checkIn_list
    countDic = dict()
    for checkIn_entry in checkIn_list:
        if checkIn_entry[1]>=start_time and checkIn_entry[1]<=end_time:
            if checkIn_entry[0] not in countDic.keys():
                countDic[checkIn_entry[0]] = 1
            else:
                countDic[checkIn_entry[0]] += 1

    tupleMax = max(countDic.items(), key = lambda k: k[1])
    return tupleMax[1]

def stayTimeInRegion(xCen, yCen, r, E_t0, initPro, uid):
    global checkIn_list
    newList = sorted(checkIn_list, key = itemgetter(0)) #TO DO improvement algorithmically : consume only required checkIn_list
    timeFilteredList = []
    for entry in newList:
        if uid < entry[0]:
            break
        elif uid == entry[0]:
            if entry[1]>=E_t0 and entry[1]<=(E_t0 + initPro):
                timeFilteredList.append(entry)
    if not timeFilteredList:
        return 0
    timeList = sorted(timeFilteredList, key = itemgetter(1))
    initial = -1
    total = 0.0
    for i in range(len(timeList)):
        if insideRegion(xCen, yCen, r, timeList[i][3], timeList[i][2]):
            prev_point_x = timeList[i][3]
            prev_point_y = timeList[i][2]
            last_timestamp = timeList[i][1]
            if initial == -1:
                initial = timeList[i][1]
            if i == len(timeList) - 1:
                total += E_t0 + initPro - initial
        elif initial!=-1:
            boundary_time_stamp = getTimeStampRegion(xCen, yCen, r, prev_point_x, prev_point_y,
                                                     last_timestamp, timeList[i][3], timeList[i][2], timeList[i][1])

            total += boundary_time_stamp - initial
            initial = -1
    #print "total", total
    return total

def check(checkIn_entry, ind):
    global eventType
    global influenced_list
    global user_list
    user_id = checkIn_entry[0]
    global osnOn, pwOn
    status = getSwitchStatus()
    osnOn = status[1]
    pwOn = status[2]
    influenced_val = 0
    if osnOn:
        influenced_val = social_check(checkIn_entry, influenced_list)
    if influenced_val==0 and pwOn:
        influenced_val = physical_check(checkIn_entry, influenced_list, ind)
    #influenced_bool = ((osnOn and social_check(checkIn_entry, influenced_list)) or (pwOn and physical_check(checkIn_entry, influenced_list, ind)))
    if influenced_val!=0:
        user_list[user_id]['influenced_bit'] = influenced_val
        polarity = influenced_val
        if polarity==1:
            online_share_prob = osn_share_prob(eventType, user_list[user_id]['interests_list'])
        elif polarity==-1:
            online_share_prob = osn_share_prob(eventType, user_list[user_id]['neg_interests_list'])
        else:
            print "polarity screwed in simulation.py online share"
        random_num = random.random() # between 0 to 1
        if random_num <= online_share_prob:
            user_list[user_id]['online_shared'] = 1
        if polarity==1:
            offline_share_prob = pw_share_prob(eventType, user_list[user_id]['interests_list']) #improvement: should have position too
        elif polarity==-1:
            offline_share_prob = pw_share_prob(eventType, user_list[user_id]['neg_interests_list'])
        else:
            print "polarity screwed in simulation.py offline share"
        random_num = random.random()
        if random_num <= offline_share_prob:
            user_list[user_id]['offline_shared'] = 1
        return 1
    return 0

def traverse():
    global checkIn_list
    global user_list
    ind = 0
    for checkIn_entry in checkIn_list:
        user_id = checkIn_entry[0]
        validity_status = checkIn_entry[5]
        if (validity_status==0 and  user_list[user_id]['influenced_bit']==0):
            if check(checkIn_entry, ind):
                user_list[user_id]['physical_share_time_list'] = setGradientTimeList(checkIn_entry[1])
                user_list[user_id]['time_of_influence'] = checkIn_entry[1]
                checkIn_entry[5] = 1
                influenced_list.append(user_id)
                #print user_id, checkIn_entry[1], user_list[user_id]['influenced_bit']
        ind = ind + 1

def filter_checkInList(start_time, end_time):
    global checkIn_list
    #linear search right now, make it binary search later
    flag = False
    start_ind = 0
    end_ind = -1
    ind = 0
    for checkIn_entry in checkIn_list:
        if checkIn_entry[1]>=start_time and checkIn_entry[1]<=end_time:
            if flag==False:
                flag = True
                start_ind = ind
        else :
            if flag == True:
                end_ind = ind
                break
        ind = ind+1
    if flag==True:
        if end_ind < start_ind:
            end_ind = len(checkIn_list) - 1
        return start_ind, end_ind
    else :
        return 0, 0

def printNodes(influenced_list):
    global user_list
    positive_count = 0
    negative_count = 0
    for influenced_node in influenced_list:
        polarity = user_list[influenced_node]['influenced_bit']
        if polarity<0:
            negative_count = negative_count + 1
        elif polarity>0:
            positive_count = positive_count + 1
    print "Positive Nodes: ", positive_count, ", Negative Nodes: ", negative_count

def F(pos):
    random.seed(10)
    print "position", pos[0], pos[1]
    global influenced_list, checkIn_list, user_list, n_users
    global init_on, osn_on, pw_on
    global initPro, addPro

    status = getSwitchStatus()
    initOn = status[0]
    osnOn = status[1]
    pwOn = status[2]
    initPro = getInitPro()
    addPro = getAddPro()
    print initOn, osnOn, pwOn, initPro, addPro
    graph_object.initialize(BRIGHTKITE_DATASET)
    return_pos_time.initialize(BRIGHTKITE_DATASET)
    checkIn_list = checkIn_object.getCheckInList(BRIGHTKITE_DATASET)
    user_list = user_object.reset(user_list)
    n_users = len(user_list)
    influenced_list = list()
    if initOn:
        new_influenced = initial_propogation(pos[0], pos[1], e_t0, e_t0+initPro)
        printNodes(influenced_list)
    if new_influenced!=None:
        start_ind, end_ind = filter_checkInList(e_t0+initPro, e_t0+initPro+addPro)
        checkIn_list = checkIn_list[start_ind: end_ind + 1]
        #time.sleep(10)
        traverse()
    #print len(influenced_list)
    printNodes(influenced_list)
    return len(influenced_list)

#start = time.clock()
F((0.09916773323165684, 0.3422742228921536))
#print time.clock() - start

#for influenced_user in influenced_list:
#    print(str(influenced_user) , ':' , user_list[influenced_user]['time_of_influence'])

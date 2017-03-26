import checkIn_object
import user_object
from user_object import setGradientTimeList
from constants import *
import graph_object
from maths import osn_share_prob, osn_inf_prob, pw_share_prob, phy_inf_prob, insideRegion, init_inf_prob, eucledianDist
import random
import time
from operator import itemgetter
from return_pos_time import get_pos
import return_pos_time

eventType = ['Painting', 'Ballooning', 'Surfing']

random.seed(10)

global influenced_list, checkIn_list, n_users, user_list

global initOn, osnOn, pwOn
global initPro, addPro, eR0

def social_check(checkIn_entry , influenced):
    global eventType
    user_id_receiver = checkIn_entry[0]
    checkIn_time = checkIn_entry[1]
    description_count = 0
    for user_id_sender in influenced:
        if not user_list[user_id_sender]['online_shared']:
            continue
        if(graph_object.checkUnDirectedEdge(user_id_sender, user_id_receiver)):
            time_of_influence_sender = user_list[user_id_sender]['time_of_influence']
            if (time_of_influence_sender <= checkIn_time): # less than or less than equal to?
                    description_count = description_count + 1
    if description_count > 0:
        rec_prob = osn_inf_prob(eventType, user_list[user_id_receiver]['interests_list'], description_count)
        random_num = random.random()
        if random_num <= rec_prob:
            return True
    return False

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
        if time<=(timestamp+ pow(10, -10)) and time>=(timestamp): #check the dependency with this buffer time
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
        if insideRegion(sender_position[0], sender_position[1], rp, receiver_lon, receiver_lat):
            if not sharedTimeCheck(user_id_sender, checkIn_entry[1]):
                continue
            isOnlineFriend = graph_object.checkUnDirectedEdge(user_id_sender, user_id_receiver)
            rec_prob = phy_inf_prob(eventType, user_list[user_id_receiver]['interests_list'], isOnlineFriend)
            random_num = random.random()
            if random_num <= rec_prob:
                return True
    return False

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

def initial_propogation(event_lon, event_lat, start_time, end_time):
    global eventType, influenced_list, user_list
    global initPro, eR0
    eR0 = getInitInfReg()
    initPro = getInitPro()
    users_region_list = get_initial_users(event_lon, event_lat, eR0, start_time, end_time)  #TODO improvement get stayTimeInRegion here only
    print "length", len(users_region_list)
    for user_id in users_region_list:
        timeInRegion = stayTimeInRegion(event_lon, event_lat, eR0, e_t0, initPro, user_id)
        inf_prob = init_inf_prob(eventType, user_list[user_id]['interests_list'], timeInRegion)
        random_num = random.random() # between 0 to 1
        if random_num <= inf_prob:
            user_list[user_id]['influenced_bit'] = 1
            user_list[user_id]['time_of_influence'] = end_time
            influenced_list.append(user_id)
            online_share_prob = osn_share_prob(eventType, user_list[user_id]['interests_list'])
            random_num = random.random() # between 0 to 1
            user_list[user_id]['physical_share_time_list'] = setGradientTimeList(end_time)
            if random_num <= online_share_prob:
                user_list[user_id]['online_shared'] = 1
            offline_share_prob = pw_share_prob(eventType, user_list[user_id]['interests_list']) #improvement: should have position too
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
    influenced_bool = ((osnOn and social_check(checkIn_entry, influenced_list)) or (pwOn and physical_check(checkIn_entry, influenced_list, ind)))
    if influenced_bool:
        online_share_prob = osn_share_prob(eventType, user_list[user_id]['interests_list'])
        random_num = random.random() # between 0 to 1
        if random_num <= online_share_prob:
            user_list[user_id]['online_shared'] = 1
        offline_share_prob = pw_share_prob(eventType, user_list[user_id]['interests_list']) #improvement: should have position too
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
                user_list[user_id]['influenced_bit'] = 1
                user_list[user_id]['physical_share_time_list'] = setGradientTimeList(checkIn_entry[1])
                user_list[user_id]['time_of_influence'] = checkIn_entry[1]
                checkIn_entry[5] = 1
                influenced_list.append(user_id)
                print user_id, checkIn_entry[1]
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

def F(pos):
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
    user_list = user_object.main(BRIGHTKITE_DATASET, e_t0, initPro, addPro)
    n_users = len(user_list)
    influenced_list = list()
    if initOn:
        new_influenced = initial_propogation(pos[0], pos[1], e_t0, e_t0+initPro)
        print len(influenced_list)
    if new_influenced!=None:
        start_ind, end_ind = filter_checkInList(e_t0+initPro, e_t0+initPro+addPro)
        checkIn_list = checkIn_list[start_ind: end_ind + 1]
        #time.sleep(10)
        traverse()
    print len(influenced_list)
    return len(influenced_list)

F((0.09916773323165684, 0.3422742228921536))
#for influenced_user in influenced_list:
#    print(str(influenced_user) , ':' , user_list[influenced_user]['time_of_influence'])

import checkIn_object
import user_object
from constants import BRIGHTKITE_DATASET, GOWALLA_DATASET
from constants import e_t0, init_pro, add_pro, rp, e_r0, e_lon, e_lat
import graph_object
from maths import osn_share_prob, osn_inf_prob, pw_share_prob, phy_inf_prob, insideRegion, init_inf_prob
import random
from operator import itemgetter

eventType = 'Puppetry'

checkIn_list = checkIn_object.getCheckInList(BRIGHTKITE_DATASET)
user_list = user_object.main(BRIGHTKITE_DATASET, e_t0, init_pro, add_pro)
n_users = len(user_list)
influenced_list = list()
graph_object.initialize(BRIGHTKITE_DATASET)


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
    low_time = receiver_time - 0.0001
    high_time = receiver_time + 0.0001
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
    
def physical_check(checkIn_entry , influenced, ind):
    global eventType
    global user_list
    user_id_receiver = checkIn_entry[0]
    checkIn_time = checkIn_entry[1]
    user_id_rejected_set = set()
    # do it user wise or checkIn wise
    for user_id_sender in influenced:
        if not user_list[user_id_sender]['offline_shared']:
            continue
        ind_s = offline_edge(user_id_sender, checkIn_entry, ind)
        if ind_s != -1:
            #validTimeCheck() #check through share time list
            isOnlineFriend = graph_object.checkUnDirectedEdge(user_id_sender, user_id_receiver)
            rec_prob = phy_inf_prob(eventType, user_list[user_id_receiver]['interests_list'], isOnlineFriend)
            random_num = random.random()
            if random_num <= rec_prob:
                return True
    return False
    
def get_initial_users(event_lon, event_lat, start_time, end_time):
    global checkIn_list
    users_set = set()
    for checkIn_entry in checkIn_list:
        user_id = checkIn_entry[0]
        if user_id in users_set:
            continue
        if checkIn_entry[1]>=start_time and checkIn_entry[1]<=end_time:
            if insideRegion(event_lon, event_lat, rp, checkIn_entry[3], checkIn_entry[2]):
                users_set.add(checkIn_entry[0])
    users_set = list(users_set)
    users_set.sort()
    return users_set
    
def initial_propogation(event_lon, event_lat, start_time, end_time):
    global eventType
    global influenced_list
    global user_list
    users_region_list = get_initial_users(event_lon, event_lat, start_time, end_time)  #TODO improvement get stayTimeInRegion here only
    #print users_region_list
    for user_id in users_region_list:
        timeInRegion = stayTimeInRegion(event_lon, event_lat, e_r0, e_t0, init_pro, user_id)
        print "time " + str(timeInRegion)
        inf_prob = init_inf_prob(eventType, user_list[user_id]['interests_list'], timeInRegion)
        random_num = random.random() # between 0 to 1
        if random_num <= inf_prob:
            user_list[user_id]['influenced_bit'] = 1
            user_list[user_id]['time_of_influence'] = end_time 
            influenced_list.append(user_id)
            print user_id, end_time
            online_share_prob = osn_share_prob(eventType, user_list[user_id]['interests_list'])
            random_num = random.random() # between 0 to 1
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

def stayTimeInRegion(xCen, yCen, r, E_t0, init_pro, uid):
    global checkIn_list
    newList = sorted(checkIn_list, key = itemgetter(0)) #TO DO improvement algorithmically : consume only required checkIn_list
    #print newList[:50]
    timeFilteredList = []
    #print uid, newList[0][0]
    for entry in newList:
        if uid < entry[0]:
            #print "tadam"
            break
        elif uid == entry[0]:
            if entry[1]>=E_t0 and entry[1]<=(E_t0 + init_pro):
                timeFilteredList.append(entry)
        #print timeFilteredList
    if not timeFilteredList:
        return 0
    #print "todo"
    timeList = sorted(timeFilteredList, key = itemgetter(1))
    initial = -1
    total = 0.0
    for i in range(len(timeList)):
        #print "yo"
        if insideRegion(xCen, yCen, r, timeList[i][3], timeList[i][2]):
            #print "hello"
            if initial == -1:
                initial = timeList[i][1]            
            if i == len(timeList) - 1:
                total += E_t0 + init_pro - initial                  
        elif initial!=-1:
            total += timeList[i][1] - initial
            initial = -1
    return total
            
def check(checkIn_entry, ind):
    global eventType
    global influenced_list
    global user_list
    user_id = checkIn_entry[0]
    influenced_bool = (social_check(checkIn_entry, influenced_list) or physical_check(checkIn_entry, influenced_list, ind))
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
    #print "checkIN"
    print len(checkIn_list)
    for checkIn_entry in checkIn_list:
        #print "traverse"
        user_id = checkIn_entry[0]
        validity_status = checkIn_entry[5]
        if (validity_status==0 and  user_list[user_id]['influenced_bit']==0):
            if check(checkIn_entry, ind):
                user_list[user_id]['influenced_bit'] = 1
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
    
new_influenced = initial_propogation(e_lon, e_lat, e_t0, e_t0+init_pro)
print influenced_list
if new_influenced!=None:
    start_ind, end_ind = filter_checkInList(e_t0+init_pro, e_t0+init_pro+add_pro)
    print "indexes"
    print start_ind, end_ind
    checkIn_list = checkIn_list[start_ind: end_ind + 1]
    traverse()

for influenced_user in influenced_list:
    print(str(influenced_user) , ':' , user_list[influenced_user]['time_of_influence'])
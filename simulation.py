import checkIn_object
import user_object
from constants import BRIGHTKITE_DATASET, GOWALLA_DATASET
from constants import e_t0, init_pro, add_pro
import graph_object
from maths import osn_share_prob, osn_inf_prob, pw_share_prob
import random
######################		CONSTANTS		##############

eventType = 'Puppetry'

checkIn_list = checkIn_object.getCheckInList(BRIGHTKITE_DATASET)
user_list = user_object.main(BRIGHTKITE_DATASET, e_t0, init_pro, add_pro)
n_users = len(user_list)
i_list = [0]
graph_object.initialize(BRIGHTKITE_DATASET)


######################		FUNCTIONS		######################
def getKey(item):
    return item[0]

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
        if random_num >= rec_prob:
            return True
    return False

def offline_edge(user_id_sender, checkIn_entry, ind):
    global checkIn_list
    user_id_receiver = checkIn_entry[0]
    receiver_time = checkIn_entry[1]
    receiver_lat = checkIn_entry[2]
    receiver_lon = checkIn_entry[3]
    low_time = buffer_fun(receiver_time, 0)
    high_time = buffer_fun(receiver_time, 1)
    while True:
        ind = ind - 1
        if ind<0 or low_time>checkIn_list[ind][1]:
            break
        if checkIn_list[ind][0] == user_id_sender 
    
def physical_check(checkIn_entry , influenced, ind):
    global eventType
    user_id_receiver = checkIn_entry[0]
    checkIn_time = checkIn_entry[1]
    user_id_rejected_set = set()
    for user_id_sender in influenced:
        if not user_list[user_id_sender]['offline_shared']:
            continue
        if(offline_edge(user_id_sender, checkIn_entry, ind)):
	return True

def check(checkIn_entry, ind):
	global eventType
    user_id = checkIn_entry[0]
    res = 0
	for influenced in i_list:
		res = (social_check(checkIn_entry , influenced) or physical_check(checkIn_entry , influenced, ind))
		if res:
            online_share_prob = osn_share_prob(eventType, user_list[user_id]['interests_list'])
            random_num = random.random() # between 0 to 1
            if random_num >= online_share_prob:
                user_list[user_id]['online_shared'] = 1
			offline_share_prob = pw_share_prob(eventType, user_list[user_id]['interests_list']) #improvement: should have position too
            random_num = random.random()
            if random_num >= offline_share_prob:
                user_list[user_id]['offline_shared'] = 1
            return 1
	return 0

def traverse():
	val = []
    ind = 0
	for e in checkin_list:
		if ( e[3]==0 and influenced_bits[e[1]]==0 ):
			print(e[1],':',e[0])
			if check(e, ind):
				val = e
				influenced_bits[e[1]]=1
				Ti[e[1]] = e[0]
				i_list.append(e[1])
				e[3]=1
				#print(val)
				return val
        ind = ind + 1
	return None

######################		EXE		#######################

#checkin_list.sort()
#print(checkin_list)

for i in range(0,n_users):
	influenced_bits.append(0)

new_influenced = traverse()

while new_influenced!=None:
	new_influenced = traverse()

for i in i_list:
	print(str(i) , ':' , Ti[i])




